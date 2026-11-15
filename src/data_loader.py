
from pathlib import Path

import pandas as pd
import yfinance as yf


# ETF configuration
ETF_TICKERS = ["SPY", "IVV", "VOO"]

START_DATE = "2025-11-14"
END_DATE = "2026-11-14"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SNAPSHOT_PATH = (
    PROJECT_ROOT
    / "data"
    / "etf_adjusted_prices_2025-11-14_2026-11-13.csv"
)


def load_etf_data(source="snapshot"):
    """
    Load ETF market data from a saved snapshot
    or download it from Yahoo Finance.

    Returns:
        DataFrame with ticker-level columns,
        matching the existing yfinance structure.

    source:
        "snapshot" - load saved historical prices
        "yahoo"    - download historical prices
    """

    if source == "snapshot":

        print("Loading ETF data from saved snapshot...")

        if not SNAPSHOT_PATH.is_file():
            raise FileNotFoundError(
                f"Snapshot not found: {SNAPSHOT_PATH}"
            )

        # Read saved adjusted closing prices
        prices = pd.read_csv(
            SNAPSHOT_PATH,
            index_col="Date",
            parse_dates=["Date"]
        )

        # Validate columns
        if list(prices.columns) != ETF_TICKERS:
            raise ValueError(
                "Snapshot ETF columns do not match."
            )

        if prices.empty or prices.isna().any().any():
            raise ValueError(
                "Snapshot contains missing or empty data."
            )

        if not prices.index.is_unique:
            raise ValueError(
                "Duplicate snapshot dates detected."
            )

        if not prices.index.is_monotonic_increasing:
            raise ValueError(
                "Snapshot dates are not sorted."
            )

        if not (
            (prices > 0).all().all()
        ):
            raise ValueError(
                "Snapshot contains invalid prices."
            )

        # Reconstruct the ticker / Close structure
        # expected by existing analytics scripts
        data = pd.concat(
            {
                ticker: pd.DataFrame({
                    "Close": prices[ticker]
                })
                for ticker in ETF_TICKERS
            },
            axis=1
        )

        return data

    elif source == "yahoo":

        print("Downloading ETF data from Yahoo Finance...")

        data = yf.download(
            tickers=ETF_TICKERS,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=True,
            progress=False,
            group_by="ticker"
        )

        if data.empty:
            raise ValueError(
                "Yahoo Finance returned no data."
            )

        return data

    else:
        raise ValueError(
            "source must be 'snapshot' or 'yahoo'."
        )


# Backward-compatible function
def download_etf_data(source="snapshot"):
    """
    Preserve compatibility with existing scripts.

    Defaults to the saved historical snapshot.
    """
    return load_etf_data(source=source)



def main():
    print("================================")
    print("ETF Delta One Analytics Platform")
    print("================================")

    data = download_etf_data()

    print("\nDownload successful!")

    print("\nFirst 5 rows:")
    print(data.head())

    print("\nLast 5 rows:")
    print(data.tail())

    print("\nDataset dimensions:")
    print(data.shape)

    print("\nColumn structure:")
    print(data.columns)

    print("\nSPY closing prices:")
    print(data["SPY"]["Close"].head())
    print("\nMissing closing prices by ETF:")

    for ticker in ETF_TICKERS:
        missing = data[ticker]["Close"].isna().sum()
        print(f"{ticker}: {missing} missing values")    

if __name__ == "__main__":
    main()
