
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

def calculate_tracking_error(
    etf_returns,
    benchmark_returns,
    trading_days=252
):
    """
    Calculate annualized tracking error.

    Parameters:
        etf_returns: Daily ETF returns (decimal form)
        benchmark_returns: Daily benchmark returns
        trading_days: Trading days per year

    Returns:
        Annualized tracking error (decimal form)
    """

    # Align both return series by date
    aligned = pd.concat(
        [etf_returns, benchmark_returns],
        axis=1,
        keys=["ETF", "Benchmark"]
    ).dropna()

    if len(aligned) < 2:
        raise ValueError(
            "At least two aligned observations are required."
        )

    # Calculate daily tracking differences
    tracking_diff = (
        aligned["ETF"] - aligned["Benchmark"]
    )

    # Calculate daily standard deviation
    daily_tracking_error = tracking_diff.std(ddof=1)

    # Annualize tracking error
    annualized_tracking_error = (
        daily_tracking_error * trading_days ** 0.5
    )

    return annualized_tracking_error

def calculate_beta(etf_returns, benchmark_returns):
    """
    Calculate ETF beta relative to a benchmark.

    Beta = Covariance(ETF, Benchmark)
           / Variance(Benchmark)
    """

    # Align observations by date
    aligned = pd.concat(
        [etf_returns, benchmark_returns],
        axis=1,
        keys=["ETF", "Benchmark"]
    ).dropna()

    if len(aligned) < 2:
        raise ValueError(
            "At least two observations are required."
        )

    # Calculate covariance
    covariance = aligned["ETF"].cov(
        aligned["Benchmark"]
    )

    # Calculate benchmark variance
    benchmark_variance = aligned["Benchmark"].var()

    if benchmark_variance <= 0:
        raise ValueError(
            "Benchmark variance must be positive."
        )

    # Calculate beta
    beta = covariance / benchmark_variance

    return beta


def calculate_correlation(etf_returns, benchmark_returns):
    """
    Calculate Pearson correlation between
    ETF and benchmark daily returns.
    """

    # Align observations by date
    aligned = pd.concat(
        [etf_returns, benchmark_returns],
        axis=1,
        keys=["ETF", "Benchmark"]
    ).dropna()

    if len(aligned) < 2:
        raise ValueError(
            "At least two observations are required."
        )

    correlation = aligned["ETF"].corr(
        aligned["Benchmark"]
    )

    return correlation


if __name__ == "__main__":
    main()
