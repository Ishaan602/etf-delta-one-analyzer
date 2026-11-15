
import matplotlib.pyplot as plt

from data_loader import download_etf_data, ETF_TICKERS
from tracking_metrics import (
    calculate_daily_returns,
    calculate_cumulative_returns
)


def main():
    print("Downloading ETF market data...")

    # Download historical ETF data
    data = download_etf_data()

    # Extract adjusted closing prices
    closing_prices = data.loc[
        :, [(ticker, "Close") for ticker in ETF_TICKERS]
    ].copy()

    # Simplify column names
    closing_prices.columns = ETF_TICKERS

    # Calculate daily returns
    daily_returns = calculate_daily_returns(
        closing_prices
    )

    # Calculate cumulative returns
    cumulative_returns = calculate_cumulative_returns(
        daily_returns
    )

    # Convert to percentages for display
    cumulative_pct = cumulative_returns * 100

    # Create the chart
    plt.figure(figsize=(12, 6))

    for ticker in ETF_TICKERS:
        plt.plot(
            cumulative_pct.index,
            cumulative_pct[ticker],
            label=ticker,
            linewidth=2
        )

    # Add chart labels
    plt.title(
        "S&P 500 ETF Cumulative Performance",
        fontsize=16
    )

    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")

    # Add a horizontal zero-return line
    plt.axhline(0, linestyle="--", linewidth=1)

    plt.legend()
    plt.grid(True, alpha=0.3)

    # Improve spacing
    plt.tight_layout()

    # Save the chart
    plt.savefig(
        "outputs/etf_cumulative_returns.png",
        dpi=300
    )

    print("Chart saved successfully!")

    # Display the chart
    plt.show()


if __name__ == "__main__":
    main()
