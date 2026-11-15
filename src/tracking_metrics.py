
import pandas as pd


def calculate_daily_returns(prices):
    """
    Calculate daily percentage returns from adjusted prices.

    Formula:
    Return = (Today's Price / Yesterday's Price) - 1
    """

    returns = prices.pct_change(fill_method=None)

    return returns

def calculate_cumulative_returns(daily_returns):
    """
    Calculate compounded cumulative returns.

    Formula:
    Cumulative Return = Product(1 + daily return) - 1
    """

    cumulative_returns = (
        (1 + daily_returns).cumprod() - 1
    )

    return cumulative_returns


def main():
    # Example adjusted closing prices
    sample_prices = pd.Series(
        [600, 606, 603],
        index=["Monday", "Tuesday", "Wednesday"]
    )

    print("Sample Prices:")
    print(sample_prices)

    daily_returns = calculate_daily_returns(sample_prices)

    print("\nDaily Returns (%):")
    print((daily_returns * 100).round(3))


if __name__ == "__main__":
    main()
