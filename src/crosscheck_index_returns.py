
from pathlib import Path

import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parent.parent

TR_PATH = (
    PROJECT_ROOT
    / "data"
    / "sp500_total_return_2025-11-14_2026-11-13.csv"
)


def main():
    print("=" * 50)
    print("S&P 500 Price vs Total Return Cross-Check")
    print("=" * 50)

    # Load saved total-return index
    total_return = pd.read_csv(
        TR_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )["SP500TR"]

    # Download price-return index
    price_data = yf.download(
        "^GSPC",
        start="2026-06-17",
        end="2026-07-08",
        auto_adjust=False,
        progress=False
    )

    if price_data.empty:
        raise ValueError(
            "No S&P 500 price-index data returned."
        )

    if isinstance(price_data.columns, pd.MultiIndex):
        price_index = price_data["Close"].iloc[:, 0]
    else:
        price_index = price_data["Close"]

    price_index.index = pd.to_datetime(
        price_index.index
    ).tz_localize(None).normalize()

    # Align the two index series
    combined = pd.concat(
        [
            price_index.rename("SP500"),
            total_return.rename("SP500TR")
        ],
        axis=1,
        join="inner"
    ).sort_index()

    # Calculate daily returns
    daily_returns = combined.pct_change(
        fill_method=None
    )

    # Difference in basis points
    daily_returns["TR Minus Price (bps)"] = (
        daily_returns["SP500TR"]
        - daily_returns["SP500"]
    ) * 10000

    print("\nIndex Daily Returns (%):")
    print(
        (
            daily_returns[["SP500", "SP500TR"]]
            * 100
        ).round(4).to_string()
    )

    print("\nTotal Return Minus Price Return (bps):")
    print(
        daily_returns["TR Minus Price (bps)"]
        .round(4).to_string()
    )


if __name__ == "__main__":
    main()
