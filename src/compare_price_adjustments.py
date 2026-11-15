
import yfinance as yf
import pandas as pd

TICKERS = ["SPY", "IVV", "VOO"]

# Include dates before the June dividend events
START_DATE = "2026-06-10"
END_DATE = "2026-07-06"


def main():
    print("Raw vs Adjusted ETF Return Analysis")

    raw_prices = {}
    adjusted_prices = {}

    for ticker in TICKERS:
        data = yf.Ticker(ticker).history(
            start=START_DATE,
            end=END_DATE,
            auto_adjust=False,
            actions=True
        )

        if data.empty:
            raise RuntimeError(
                f"No data returned for {ticker}"
            )

        raw_prices[ticker] = data["Close"]
        adjusted_prices[ticker] = data["Adj Close"]

    raw_prices = pd.DataFrame(raw_prices)
    adjusted_prices = pd.DataFrame(adjusted_prices)

    # Calculate daily returns
    raw_returns = raw_prices.pct_change(
        fill_method=None
    )

    adjusted_returns = adjusted_prices.pct_change(
        fill_method=None
    )

    # Compare against SPY in basis points
    raw_diff = raw_returns[["IVV", "VOO"]].sub(
        raw_returns["SPY"], axis=0
    ) * 10000

    adjusted_diff = adjusted_returns[
        ["IVV", "VOO"]
    ].sub(
        adjusted_returns["SPY"], axis=0
    ) * 10000

    # Compare the two return methodologies
    for ticker in ["IVV", "VOO"]:
        comparison = pd.DataFrame({
            "Raw Difference (bps)": raw_diff[ticker],
            "Adjusted Difference (bps)":
                adjusted_diff[ticker]
        })

        comparison["Adjustment Impact (bps)"] = (
            comparison["Adjusted Difference (bps)"]
            - comparison["Raw Difference (bps)"]
        )

        print(f"\n{ticker} vs SPY:")
        print(comparison.round(3))


if __name__ == "__main__":
    main()
