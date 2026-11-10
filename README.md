# Quant-2Week — Market Data Pipeline

A small, runnable project that teaches the mechanics a quant uses on day one:

1. **Fetch** real market data (yfinance → clean OHLCV per ticker)
2. **Compute** daily returns + descriptive statistics (skew, kurtosis, vol)
3. **Visualize** cumulative returns + return histogram vs. normal

## What's here

```
week1/
  fetch_data.py      # downloads daily OHLC for a ticker list
  analyze_data.py    # returns → stats + 2 plots
  main.py            # runs fetch → analyze end to end
  requirements.txt   # Python stack
  .gitignore         # keeps data/ and output/ out of the repo
```

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate          # venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

## Full pipeline (step by step)

### Step 1 — Fetch
`fetch_data.py` calls `yfinance.download()` for `AAPL`, `MSFT`, `GOOGL`.
yfinance returns a pandas DataFrame with a **MultiIndex column index** (each field
paired with a ticker label), so the code flattens it with:

```python
df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
```

then renames the fields to snake_case and exports a clean CSV:

```
Date,adj_close,close,high,low,open,volume
```

### Step 2 — Compute returns
`analyze_data.py` reads each CSV, parses `Date` as the index, and computes
**log returns** (`np.log(P / P.shift(1))`) — the additive measure used in every
quant pipeline (simple percentage returns are NOT additive across time).

```python
rets = np.log(df["close"] / df["close"].shift(1))
```

### Step 3 — Statistics
Per ticker it prints:
- mean / std (daily, and annualized × √252)
- **skewness** — asymmetry; equities are usually +skew
- **kurtosis** — tail weight; normal = 3. Real equities come in 3–15.

### Step 4 — Visuals
Two plots are written to `output/`:
- `cumulative_returns.png` — 3 cumulative log-return curves, one per ticker
- `returns_histogram.png` — every ticker's histogram overlayed with a fitted
  Gaussian, labelled with skew/kurtosis

## What you should understand, not just run

| Concept | What it means |
|---|---|
| Simple vs. log returns | Simple `%Δ` is easy but not additive; `ln(P/P.shift(1))` stacks cleanly |
| Skew & kurtosis | Skew = asymmetry (+ve for equities). Kurtosis = tail weight; normal=3, real equities are 3–15 → fat tails, risk models understate extremes |
| Covariance matrix | The *off-diagonal* values tell you how assets move together — this is where diversification lives |
| No-arbitrage / payout | Options pay off only above/below a strike; not an all-in-up-all-in-down instrument |

## Why `data/` and `output/` are git-ignored

Stock prices are a third party's property. This repo ships **code + statistics only**.
`data/` (raw CSVs) and `output/` (generated PNGs) are regenerated locally via
`python main.py`, so a fresh clone + `pip install` + `python main.py` produces
everything without you ever needing to download a file.

## License & notes

Academic use only. Market data belongs to its distributors. Consult a qualified
risk professional before risking real capital.

Built with:
- Python 3.12
- yfinance, pandas, matplotlib, NumPy
