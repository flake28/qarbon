"""fetch_data.py — download daily OHLC for a list of tickers via yfinance.

Saves one clean CSV per ticker into data/ (e.g. data/AAPL.csv).
yfinance returns a MultiIndex column index; this flattens it and renames the
six price fields to snake_case so every CSV has the same unique column names:
  Date, adj_close, close, high, low, open, volume
"""
import os

import pandas as pd
import yfinance as yf

TICKERS = ["AAPL", "MSFT", "GOOGL"]
START = "2024-06-01"
END = "2026-08-01"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# MultiIndex level values -> snake_case names (fixed order)
FIELD_MAP = {
    "Adj Close": "adj_close",
    "Close": "close",
    "High": "high",
    "Low": "low",
    "Open": "open",
    "Volume": "volume",
}


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    # Flatten MultiIndex columns to their price-field name.
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df = df.rename(columns=FIELD_MAP)
    # Make the date the working index, then export it as a column.
    df = df.reset_index()
    df = df.rename(columns={"index": "Date"})  # in case index name was empty
    df = df[["Date"] + [c for c in df.columns if c not in ("Date", "index")]]
    return df.sort_values("Date")


def fetch(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)
    return _clean(df)


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    for t in TICKERS:
        df = fetch(t, START, END)
        path = os.path.join(DATA_DIR, f"{t}.csv")
        df.to_csv(path, index=False)
        print(f"✓ {t}: {len(df)} rows, {df['Date'].iloc[0]} → {df['Date'].iloc[-1]}")
    print("Saved into:", DATA_DIR)


if __name__ == "__main__":
    main()
