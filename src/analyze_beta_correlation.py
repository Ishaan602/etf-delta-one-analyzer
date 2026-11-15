
import pandas as pd
import numpy as np

from data_loader import download_etf_data, ETF_TICKERS

from tracking_metrics import (
    calculate_daily_returns,
    calculate_beta,
    calculate_correlation
)


def main():
    print("================================")
    print("ETF Beta and Correlation Analysis")
    print("================================")

    # Step 1: Download historical ETF prices
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

    # Step 4: Remove first missing return
    daily_returns = daily_returns.dropna()

    # Step 5: Use SPY as our reference ETF
    spy_returns = daily_returns["SPY"]

    # Step 6: Calculate beta and correlation
    results = []

    for ticker in ["IVV", "VOO"]:

        etf_returns = daily_returns[ticker]

        beta = calculate_beta(
            etf_returns,
            spy_returns
        )

        correlation = calculate_correlation(
            etf_returns,
            spy_returns
        )

        results.append({
            "ETF": ticker,
            "Beta vs SPY": beta,
            "Correlation vs SPY": correlation
        })

    # Step 7: Display the results
    results_df = pd.DataFrame(results)
    results_df = results_df.set_index("ETF")

    print("\nBeta and Correlation Results:")
    print(results_df.round(6))

    # Step 8: Independent beta validation
    for ticker in ["IVV", "VOO"]:

        expected_beta = (
            daily_returns[ticker].cov(spy_returns)
            / spy_returns.var()
        )

        actual_beta = results_df.loc[
            ticker, "Beta vs SPY"
        ]

        assert np.isclose(
            actual_beta,
            expected_beta,
            atol=1e-10
        ), f"Beta validation failed for {ticker}"

    # Validate correlation calculations
    for ticker in ["IVV", "VOO"]:

        expected_corr = (
            daily_returns[ticker].corr(spy_returns)
        )

        actual_corr = results_df.loc[
            ticker, "Correlation vs SPY"
        ]

        assert np.isclose(
            actual_corr,
            expected_corr,
            atol=1e-10
        ), f"Correlation validation failed for {ticker}"

    print("Correlation calculations validated successfully!")
    print("\nBeta calculations validated successfully!")


if __name__ == "__main__":
    main()
