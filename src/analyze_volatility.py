
import pandas as pd
import numpy as np

from data_loader import download_etf_data, ETF_TICKERS

from tracking_metrics import (
    calculate_daily_returns,
    calculate_rolling_volatility
)


def main():
    print("================================")
    print("ETF Rolling Volatility Analysis")
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

    # Remove the first undefined return
    daily_returns = daily_returns.dropna()

    # Step 4: Calculate 20-day rolling volatility
    rolling_volatility = calculate_rolling_volatility(
        daily_returns,
        window=20
    )

    # Step 5: Convert to percentages for display
    rolling_volatility_pct = rolling_volatility * 100

    print("\nLast 5 Rolling Volatility Observations (%):")
    print(rolling_volatility_pct.tail().round(4))

    # Step 6: Extract latest volatility estimates
    latest_volatility = rolling_volatility_pct.iloc[-1]

    print("\nLatest 20-Day Annualized Volatility (%):")
    print(latest_volatility.round(4))

    # Step 7: Calculate average rolling volatility
    average_volatility = rolling_volatility_pct.mean()

    print("\nAverage 20-Day Rolling Volatility (%):")
    print(average_volatility.round(4))

    # Step 8: Find maximum rolling volatility
    maximum_volatility = rolling_volatility_pct.max()

    print("\nMaximum 20-Day Rolling Volatility (%):")
    print(maximum_volatility.round(4))

    # Step 9: Validate SPY's latest volatility
    expected_spy = (
        daily_returns["SPY"].iloc[-20:].std(ddof=1)
        * np.sqrt(252)
    )

    actual_spy = rolling_volatility["SPY"].iloc[-1]

    assert np.isclose(
        actual_spy,
        expected_spy,
        rtol=1e-10,
        atol=1e-12
    ), "SPY rolling volatility validation failed!"

    print("\nSPY rolling volatility validated successfully!")
    
    # Validate rolling volatility for every ETF
    for ticker in ETF_TICKERS:

        expected = (
            daily_returns[ticker]
            .iloc[-20:]
            .std(ddof=1)
            * np.sqrt(252)
        )

        actual = rolling_volatility[ticker].iloc[-1]

        assert np.isclose(
            actual,
            expected,
            rtol=1e-10,
            atol=1e-12
        ), f"Volatility validation failed for {ticker}!"

        print(f"{ticker} volatility validated!")

    # Identify dates of maximum rolling volatility
    print("\nDates of Maximum Rolling Volatility:")

    for ticker in ETF_TICKERS:
        max_date = rolling_volatility_pct[ticker].idxmax()

        print(
            f"{ticker}: {max_date.date()}"
        )



if __name__ == "__main__":
    main()
