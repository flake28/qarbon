"""analyze_data.py — compute returns + descriptive statistics + plots.

Reads the tickers' CSV into data/, computes daily log/simple returns,
prints a stats table, and writes two plots:
  output/cumulative_returns.png   — primary chart
  output/returns_histogram.png    — histogram + fitted normal
"""
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "data")
OUT_DIR = os.path.join(BASE, "output")


def load(ticker: str) -> pd.Series:
    df = pd.read_csv(os.path.join(DATA_DIR, f"{ticker}.csv"), index_col="Date",
                     parse_dates=True)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    # Simple daily return: pct_change; drop the first NaN row.
    rets = df["close"].pct_change().dropna()
    return rets


def describe(rets: pd.Series) -> pd.Series:
    return pd.Series({
        "mean": rets.mean(),
        "std": rets.std(ddof=0),          # ddof=0 = population std (the bias-corrected kind used in pricing)
        "skew": rets.skew(),
        "kurtosis": rets.kurtosis(),      # excess kurtosis (normal=0)
        "min": rets.min(),
        "max": rets.max(),
        "count": rets.count(),
        "n_days": len(rets),
        "n_years_approx": len(rets) / 252,
    })


def plot_cumulative(rets_by_ticker: dict[str, pd.Series], out_path: str) -> None:
    plt.figure(figsize=(10, 5))
    cumsum = pd.DataFrame(rets_by_ticker).fillna(0).cumsum()
    for col in cumsum.columns:
        plt.plot(cumsum.index, cumsum[col], label=col, linewidth=1.6)
    plt.title("Cumulative log-return indexed to 0")
    plt.xlabel("Date")
    plt.ylabel("Cumulative return (log)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✓ cumulative_returns.png")


def plot_histogram(rets_by_ticker: dict[str, pd.Series], out_path: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, (t, rets) in zip(axes, rets_by_ticker.items()):
        rets = rets.dropna()
        ax.hist(rets, bins=60, density=True, alpha=0.55, label="returns")
        # Fitted normal: pdf over the range of the data.
        mu, sigma = rets.mean(), rets.std(ddof=0)
        xs = np.linspace(rets.min(), rets.max(), 200)
        ax.plot(xs, (1 / (sigma * np.sqrt(2 * np.pi))) *
                np.exp(-0.5 * ((xs - mu) / sigma) ** 2),
                linewidth=2, label="fitted normal")
        ax.set_title(f"{t}\nskew={rets.skew():.3f}, kurt={rets.kurtosis():.3f}")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    fig.suptitle("Daily returns vs. normal distribution")
    fig.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"✓ returns_histogram.png")


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

    rets_by_ticker = {}
    for t in ["AAPL", "MSFT", "GOOGL"]:
        rets = load(t)
        rets_by_ticker[t] = rets
        stats = describe(rets)
        print(f"\n=== {t} ===")
        print(stats.round(6).to_string())

    plot_cumulative(rets_by_ticker, os.path.join(OUT_DIR, "cumulative_returns.png"))
    plot_histogram(rets_by_ticker, os.path.join(OUT_DIR, "returns_histogram.png"))
    print("\nDone. Outputs in:", OUT_DIR)


if __name__ == "__main__":
    main()
