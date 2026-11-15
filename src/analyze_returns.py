
import pandas as pd

from data_loader import download_etf_data, ETF_TICKERS
from tracking_metrics import (
    calculate_daily_returns,
    calculate_cumulative_returns
)


def main():
    print("================================")
    print("ETF Daily Returns Analysis")
    print("================================")

    # Step 1: Download historical ETF data
    data = download_etf_data()

    # Step 2: Extract adjusted closing prices
    closing_prices = pd.DataFrame({
        ticker: data[ticker]["Close"]
        for ticker in ETF_TICKERS
    })

    print("\nAdjusted Closing Prices:")
    print(closing_prices.tail())

    # Step 3: Calculate daily returns
    daily_returns = calculate_daily_returns(
        closing_prices
    )
    # Validate returns against the mathematical formula
    manual_returns = (
        closing_prices / closing_prices.shift(1)
    ) - 1

    # Compare both calculation methods
    difference = (
        daily_returns - manual_returns
    ).abs()

    max_difference = difference.max().max()

    print("\nMaximum calculation difference:")
    print(max_difference)

    assert max_difference < 1e-10, (
        "Return calculation validation failed!"
    )

    print("Return calculations validated successfully!")

    # Step 4: Convert returns to percentages
    daily_returns_pct = daily_returns * 100

    print("\nDaily Returns (%):")
    print(daily_returns_pct.tail().round(3))

    # Step 5: Check the shape
    print("\nDataset dimensions:")
    print(daily_returns.shape)

    # Calculate compounded cumulative returns
    cumulative_returns = calculate_cumulative_returns(
        daily_returns
    )

    print("\nCumulative Returns (%):")
    print((cumulative_returns.tail() * 100).round(3))

    # Compare total returns over the observation period
    total_returns = cumulative_returns.iloc[-1] * 100

    # Independently validate cumulative returns
    price_based_returns = (
        closing_prices.iloc[-1] / closing_prices.iloc[0] - 1
    ) * 100

    print("\nReturns calculated from first and last prices (%):")
    print(price_based_returns.round(3))

    # Compare against compounded daily returns
    differences = (total_returns - price_based_returns).abs()

    print("\nMaximum cumulative return difference:")
    print(differences.max())

    assert differences.max() < 1e-8, (
        "Cumulative return validation failed!"
    )

    print("Cumulative returns validated successfully!")

    print("\nTotal Return by ETF (%):")
    print(total_returns.sort_values(ascending=False).round(3))

    # Identify the highest-returning ETF
    best_etf = total_returns.idxmax()

    print(f"\nHighest-returning ETF: {best_etf}")
    print(f"Return: {total_returns[best_etf]:.3f}%")


if __name__ == "__main__":
    main()
