
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ETF_PATH = (
    PROJECT_ROOT
    / "data"
    / "etf_adjusted_prices_2025-11-14_2026-11-13.csv"
)

INDEX_PATH = (
    PROJECT_ROOT
    / "data"
    / "sp500_total_return_2025-11-14_2026-11-13.csv"
)


def main():

    print("=" * 50)
    print("Index Tracking Outlier Investigation")
    print("=" * 50)

    # Load saved data
    etf_prices = pd.read_csv(
        ETF_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    index_prices = pd.read_csv(
        INDEX_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    assert etf_prices.index.equals(
        index_prices.index
    ), "Historical dates are not aligned!"

    # Combine saved prices and index levels
    prices = pd.concat(
        [etf_prices, index_prices],
        axis=1
    )

    # Calculate daily returns
    returns = prices.pct_change(
        fill_method=None
    )

    # Focus on late June and early July
    start_date = "2026-06-22"
    end_date = "2026-07-07"

    selected_returns = returns.loc[
        start_date:end_date
    ]

    print("\nDaily Returns (%):")
    print(
        (selected_returns * 100)
        .round(4)
        .to_string()
    )

    # Calculate ETF-minus-index differences
    tracking_differences = (
        selected_returns[["SPY", "IVV", "VOO"]]
        .sub(selected_returns["SP500TR"], axis=0)
        * 10000
    )

    print("\nTracking Differences (bps):")
    print(
        tracking_differences
        .round(4)
        .to_string()
    )

    # Display raw index levels
    print("\nS&P 500 Total Return Index Levels:")
    print(
        prices["SP500TR"]
        .loc[start_date:end_date]
        .round(4)
        .to_string()
    )


if __name__ == "__main__":
    main()
