
import pandas as pd
import matplotlib.pyplot as plt

from data_loader import download_etf_data, ETF_TICKERS

from tracking_metrics import (
    calculate_daily_returns,
    calculate_rolling_volatility
)


def main():
    print("================================")
    print("ETF Rolling Volatility Visualization")
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
    ).dropna()

    # Step 4: Calculate 20-day rolling volatility
    rolling_volatility = calculate_rolling_volatility(
        daily_returns,
        window=20
    )

    # Convert decimal volatility to percentages
    rolling_volatility_pct = rolling_volatility * 100

    # Step 5: Create the chart
    fig, ax = plt.subplots(figsize=(12, 6))

    for ticker in ETF_TICKERS:
        ax.plot(
            rolling_volatility_pct.index,
            rolling_volatility_pct[ticker],
            label=ticker,
            linewidth=1.8
        )

    # Step 6: Add labels and formatting
    ax.set_title(
        "S&P 500 ETF 20-Day Rolling Volatility",
        fontsize=16
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Annualized Volatility (%)")

    ax.legend()
    ax.grid(True, alpha=0.3)

    # Step 7: Highlight the SPY volatility peak
    peak_date = rolling_volatility_pct["SPY"].idxmax()
    peak_value = rolling_volatility_pct["SPY"].max()

    ax.scatter(
        peak_date,
        peak_value,
        color="black",
        s=45,
        zorder=5
    )

    ax.annotate(
        f"SPY peak: {peak_value:.2f}%",
        xy=(peak_date, peak_value),
        xytext=(-110, -35),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->"},
        fontsize=10
    )

    # Step 8: Save and display
    fig.tight_layout()

    fig.savefig(
        "outputs/etf_rolling_volatility.png",
        dpi=300,
        bbox_inches="tight"
    )

    print("\nChart saved successfully!")
    print("outputs/etf_rolling_volatility.png")

    plt.show()


if __name__ == "__main__":
    main()
