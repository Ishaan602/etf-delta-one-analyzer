
from pathlib import Path

import numpy as np
import pandas as pd

from tracking_metrics import calculate_tracking_error


# ---------------------------------------
# CONFIGURATION
# ---------------------------------------

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

ETF_TICKERS = ["SPY", "IVV", "VOO"]

TRADING_DAYS = 252


def main():

    print("=" * 50)
    print("ETF Index-Relative Tracking Analysis")
    print("=" * 50)

    # 1. Load saved ETF prices
    etf_prices = pd.read_csv(
        ETF_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    # 2. Load saved benchmark levels
    index_prices = pd.read_csv(
        INDEX_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    # 3. Verify matching dates
    assert etf_prices.index.equals(
        index_prices.index
    ), "ETF and benchmark dates do not match!"

    # 4. Combine prices and index levels
    combined_prices = pd.concat(
        [etf_prices, index_prices],
        axis=1
    )

    expected_columns = ETF_TICKERS + ["SP500TR"]

    assert list(combined_prices.columns) == expected_columns, (
        "Unexpected price columns!"
    )

    assert len(combined_prices) == 251, (
        "Unexpected number of observations!"
    )

    assert np.isfinite(
        combined_prices.to_numpy(dtype=float)
    ).all(), "Invalid price observations!"

    assert (combined_prices > 0).all().all(), (
        "Nonpositive price observations!"
    )

    # 5. Calculate aligned daily returns
    daily_returns = combined_prices.pct_change(
        fill_method=None
    ).iloc[1:]

    assert len(daily_returns) == 250, (
        "Expected 250 daily returns!"
    )

    assert daily_returns.notna().all().all(), (
        "Missing daily returns!"
    )

    # 6. Extract benchmark returns
    benchmark_returns = daily_returns["SP500TR"]

    # 7. Calculate cumulative benchmark return
    benchmark_total_return = (
        combined_prices["SP500TR"].iloc[-1]
        / combined_prices["SP500TR"].iloc[0]
        - 1
    )

    # 8. Calculate tracking metrics for each ETF
    results = []

    daily_differences = pd.DataFrame(
        index=daily_returns.index
    )

    for ticker in ETF_TICKERS:

        etf_returns = daily_returns[ticker]

        # Daily ETF-minus-index return differences
        differences = (
            etf_returns - benchmark_returns
        )

        daily_differences[ticker] = differences * 10000

        # ETF cumulative return
        etf_total_return = (
            combined_prices[ticker].iloc[-1]
            / combined_prices[ticker].iloc[0]
            - 1
        )

        # Cumulative tracking difference (bps)
        cumulative_difference = (
            etf_total_return - benchmark_total_return
        ) * 10000

        # Mean daily tracking difference (bps)
        mean_daily_difference = (
            differences.mean() * 10000
        )

        # Annualized tracking error (%)
        tracking_error = calculate_tracking_error(
            etf_returns,
            benchmark_returns
        ) * 100

        # Maximum absolute daily deviation (bps)
        max_daily_deviation = (
            differences.abs().max() * 10000
        )

        results.append({
            "ETF": ticker,
            "Cumulative Difference (bps)":
                cumulative_difference,
            "Annualized Tracking Error (%)":
                tracking_error,
            "Mean Daily Difference (bps)":
                mean_daily_difference,
            "Max Absolute Daily Deviation (bps)":
                max_daily_deviation
        })

    # 9. Create summary DataFrame
    report = pd.DataFrame(results).set_index("ETF")

    # 10. Display results
    print("\nIndex-Relative Tracking Metrics:")
    print(report.round(4).to_string())

    # 11. Display recent daily differences
    print("\nLast 5 Daily Differences (bps):")
    print(daily_differences.tail().round(4))

    # 12. Validate tracking error independently
    for ticker in ETF_TICKERS:

        expected_te = (
            daily_differences[ticker].std(ddof=1)
            / 10000
            * np.sqrt(TRADING_DAYS)
            * 100
        )

        actual_te = report.loc[
            ticker,
            "Annualized Tracking Error (%)"
        ]

        assert np.isclose(
            actual_te,
            expected_te,
            rtol=1e-10,
            atol=1e-12
        ), f"Tracking error validation failed for {ticker}!"

    # 13. Validate cumulative tracking differences
    expected_cumulative = (
        combined_prices.iloc[-1]
        / combined_prices.iloc[0]
        - 1
    ) * 100

    for ticker in ETF_TICKERS:

        expected_difference = (
            expected_cumulative[ticker]
            - expected_cumulative["SP500TR"]
        ) * 100

        actual_difference = report.loc[
            ticker,
            "Cumulative Difference (bps)"
        ]

        assert np.isclose(
            actual_difference,
            expected_difference,
            rtol=1e-10,
            atol=1e-10
        ), f"Cumulative difference validation failed for {ticker}!"

    # ---------------------------------------
    # LARGEST DAILY TRACKING DEVIATIONS
    # ---------------------------------------

    print("\nLargest Daily Tracking Deviations:")

    for ticker in ETF_TICKERS:

        differences = daily_differences[ticker]

        # Identify five largest absolute deviations
        largest_dates = (
            differences.abs()
            .nlargest(5)
            .index
        )

        # Retrieve signed differences on those dates
        largest_deviations = differences.loc[
            largest_dates
        ]

        print(f"\n{ticker} vs. SP500TR:")
        print(largest_deviations.round(4))

    # ---------------------------------------
    # COMMON OUTLIER SENSITIVITY ANALYSIS
    # ---------------------------------------

    print("\nCommon Outlier Sensitivity Analysis")
    print("=" * 45)

    # Two largest common deviation dates
    excluded_dates = pd.to_datetime([
        "2026-06-26",
        "2026-06-29"
    ])

    # Remove the same dates for every ETF
    filtered_differences = daily_differences.drop(
        index=excluded_dates,
        errors="raise"
    )

    print(
        "\nOriginal observations:",
        len(daily_differences)
    )

    print(
        "Filtered observations:",
        len(filtered_differences)
    )

    print(
        "Excluded observations:",
        len(daily_differences) - len(filtered_differences)
    )

    sensitivity_results = []

    for ticker in ETF_TICKERS:

        # Original annualized tracking error
        full_te = report.loc[
            ticker,
            "Annualized Tracking Error (%)"
        ]

        # Convert filtered differences from bps
        # back to decimal daily returns
        filtered_decimal = (
            filtered_differences[ticker] / 10000
        )

        # Recalculate annualized tracking error
        filtered_te = (
            filtered_decimal.std(ddof=1)
            * np.sqrt(TRADING_DAYS)
            * 100
        )

        # Percentage reduction
        reduction = (
            (full_te - filtered_te)
            / full_te
            * 100
        )

        sensitivity_results.append({
            "ETF": ticker,
            "Full TE (%)": full_te,
            "Filtered TE (%)": filtered_te,
            "Reduction (%)": reduction
        })

    sensitivity_df = pd.DataFrame(
        sensitivity_results
    ).set_index("ETF")

    print("\nTracking Error Sensitivity:")
    print(sensitivity_df.round(4).to_string())

    print("\nAll index-tracking validations passed!")


if __name__ == "__main__":
    main()
