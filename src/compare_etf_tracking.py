
import pandas as pd
import numpy as np

from data_loader import download_etf_data, ETF_TICKERS

from tracking_metrics import (
    calculate_daily_returns,
    calculate_tracking_error
)


def main():
    print("================================")
    print("ETF Relative Tracking Analysis")
    print("================================")

    # Step 1: Download historical ETF data
    data = download_etf_data()

    # Step 2: Extract adjusted closing prices
    closing_prices = pd.DataFrame({
        ticker: data[ticker]["Close"]
        for ticker in ETF_TICKERS
    })

    # Step 3: Calculate daily returns
    daily_returns = calculate_daily_returns(
        closing_prices
    )

    # Step 4: Use SPY as the reference ETF
    reference_returns = daily_returns["SPY"]

    # Step 5: Compare IVV and VOO against SPY
    results = []

    for ticker in ["IVV", "VOO"]:

        etf_returns = daily_returns[ticker]

        tracking_error = calculate_tracking_error(
            etf_returns,
            reference_returns
        )

        # Daily differences in basis points
        differences_bps = (
            etf_returns - reference_returns
        ) * 10000

        results.append({
            "ETF": ticker,
            "Annualized Relative TE (%)":
                tracking_error * 100,
            "Mean Daily Difference (bps)":
                differences_bps.mean(),
            "Max Absolute Daily Difference (bps)":
                differences_bps.abs().max()
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.set_index("ETF")
        # Validate relative tracking error for IVV
    ivv_diff = (
        daily_returns["IVV"] - daily_returns["SPY"]
    ).dropna()

    expected_ivv_te = (
        ivv_diff.std(ddof=1) * np.sqrt(252)
    )

    actual_ivv_te = calculate_tracking_error(
        daily_returns["IVV"],
        daily_returns["SPY"]
    )

    assert np.isclose(
        actual_ivv_te,
        expected_ivv_te,
        rtol=1e-10,
        atol=1e-12
    ), "IVV tracking error validation failed!"

    print("\nIVV relative tracking error validated!")
    print("\nRelative Tracking Metrics:")
    print(results_df.round(4))

    # Inspect the most recent daily differences
    daily_diff_bps = (
        daily_returns[["IVV", "VOO"]]
        .sub(reference_returns, axis=0)
        * 10000
    )

    print("\nLast 5 Daily Differences (bps):")
    print(daily_diff_bps.tail().round(3))
    
    # Identify the five largest deviations for each ETF
    print("\nLargest Daily Tracking Deviations:")

    for ticker in ["IVV", "VOO"]:

        # Find dates with the largest absolute differences
        largest_dates = (
            daily_diff_bps[ticker]
            .abs()
            .nlargest(5)
            .index
        )

        # Retrieve the signed differences on those dates
        largest_deviations = daily_diff_bps.loc[
            largest_dates, ticker
        ]

        print(f"\n{ticker} vs. SPY:")
        print(largest_deviations.round(3))
        
    # ---------------------------------------
    # OUTLIER SENSITIVITY ANALYSIS
    # ---------------------------------------

    print("\n================================")
    print("Outlier Sensitivity Analysis")
    print("================================")

    # Dates where large deviations occurred
    start_date = "2026-06-25"
    end_date = "2026-07-01"

    # Create a mask identifying those dates
    outlier_period = (
        (daily_returns.index >= start_date) &
        (daily_returns.index <= end_date)
    )

    # Exclude the selected period
    filtered_returns = daily_returns.loc[
        ~outlier_period
    ]

    for ticker in ["IVV", "VOO"]:

        # Tracking error using all observations
        full_te = calculate_tracking_error(
            daily_returns[ticker],
            daily_returns["SPY"]
        )

        # Tracking error excluding the selected period
        filtered_te = calculate_tracking_error(
            filtered_returns[ticker],
            filtered_returns["SPY"]
        )

        # Percentage reduction
        reduction = (
            (full_te - filtered_te) / full_te
        ) * 100

        print(f"\n{ticker} vs. SPY")

        print(
            f"Full Sample TE: {full_te * 100:.4f}%"
        )

        print(
            f"Filtered TE: {filtered_te * 100:.4f}%"
        )

        print(
            f"Reduction: {reduction:.2f}%"
        )

    print(
        "\nExcluded observations:",
        outlier_period.sum()
    )
    
    # ---------------------------------------
    # TRACKING DIFFERENCE REVERSAL ANALYSIS
    # ---------------------------------------

    print("\n================================")
    print("Tracking Difference Reversal Analysis")
    print("================================")

    start_date = "2026-06-25"
    end_date = "2026-07-01"

    period_returns = daily_returns.loc[
        start_date:end_date
    ]

    for ticker in ["IVV", "VOO"]:

        # Daily return differences in basis points
        differences = (
            period_returns[ticker]
            - period_returns["SPY"]
        ) * 10000

        # Sum of daily return differences
        sum_differences = differences.sum()

        # Compounded ETF and SPY returns
        etf_total = (
            (1 + period_returns[ticker]).prod() - 1
        )

        spy_total = (
            (1 + period_returns["SPY"]).prod() - 1
        )

        # Compounded return difference in basis points
        compounded_difference = (
            etf_total - spy_total
        ) * 10000

        # Gross magnitude of daily deviations
        gross_deviations = differences.abs().sum()

        print(f"\n{ticker} vs. SPY")

        print(
            f"Sum of Daily Differences: "
            f"{sum_differences:.3f} bps"
        )

        print(
            f"Compounded Return Difference: "
            f"{compounded_difference:.3f} bps"
        )

        print(
            f"Sum of Absolute Daily Deviations: "
            f"{gross_deviations:.3f} bps"
        )
    
    # ---------------------------------------
    # LAGGED TRACKING DIFFERENCE ANALYSIS
    # ---------------------------------------

    print("\n================================")
    print("Lagged Tracking Difference Analysis")
    print("================================")

    for ticker in ["IVV", "VOO"]:

        # Daily return differences in basis points
        differences = (
            daily_returns[ticker]
            - daily_returns["SPY"]
        ) * 10000

        # Compare today's difference with the next day's
        lagged_data = pd.DataFrame({
            "Today": differences,
            "Next Day": differences.shift(-1)
        }).dropna()

        # Correlation between consecutive differences
        lag_one_correlation = (
            lagged_data["Today"]
            .corr(lagged_data["Next Day"])
        )

        # How often consecutive differences change sign
        opposite_signs = (
            lagged_data["Today"]
            * lagged_data["Next Day"]
        ) < 0

        reversal_rate = opposite_signs.mean() * 100

        print(f"\n{ticker} vs. SPY")

        print(
            f"Lag-1 Correlation: "
            f"{lag_one_correlation:.4f}"
        )

        print(
            f"Next-Day Sign Reversal Rate: "
            f"{reversal_rate:.2f}%"
        )

        print(
            f"Observation Pairs: "
            f"{len(lagged_data)}"
        )
    
    # ---------------------------------------
    # ROBUSTNESS CHECK: EXCLUDE LATE JUNE
    # ---------------------------------------

    print("\n================================")
    print("Filtered Lag Analysis")
    print("================================")

    excluded_start = "2026-06-25"
    excluded_end = "2026-07-01"

    for ticker in ["IVV", "VOO"]:

        differences = (
            daily_returns[ticker]
            - daily_returns["SPY"]
        ) * 10000

        # Construct consecutive-day pairs FIRST
        pairs = pd.DataFrame({
            "Today": differences,
            "Next Day": differences.shift(-1)
        }).dropna()

        # Identify dates in the excluded period
        excluded_dates = (
            (pairs.index >= excluded_start) &
            (pairs.index <= excluded_end)
        )

        # Also exclude pairs whose next day is excluded
        next_dates = differences.index.to_series().shift(-1)
        next_dates = next_dates.reindex(pairs.index)

        next_excluded = (
            (next_dates >= excluded_start) &
            (next_dates <= excluded_end)
        )

        # Retain pairs with neither date excluded
        filtered_pairs = pairs.loc[
            ~(excluded_dates | next_excluded)
        ]

        filtered_corr = (
            filtered_pairs["Today"]
            .corr(filtered_pairs["Next Day"])
        )

        filtered_reversal = (
            (
                filtered_pairs["Today"]
                * filtered_pairs["Next Day"]
            ) < 0
        ).mean() * 100

        print(f"\n{ticker} vs. SPY")

        print(
            f"Filtered Lag-1 Correlation: "
            f"{filtered_corr:.4f}"
        )

        print(
            f"Filtered Reversal Rate: "
            f"{filtered_reversal:.2f}%"
        )

        print(
            f"Remaining Observation Pairs: "
            f"{len(filtered_pairs)}"
        )







if __name__ == "__main__":
    main()
