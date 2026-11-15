
import pandas as pd
import yfinance as yf


ETF_TICKERS = ["SPY", "IVV", "VOO"]

START_DATE = "2026-06-17"
END_DATE = "2026-07-08"


def main():

    print("=" * 50)
    print("ETF Raw vs Adjusted Price Cross-Check")
    print("=" * 50)

    for ticker in ETF_TICKERS:

        print(f"\n{'=' * 45}")
        print(f"{ticker} Price Investigation")
        print(f"{'=' * 45}")

        # Download raw and adjusted historical prices
        data = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=False,
            actions=True,
            progress=False
        )

        if data.empty:
            print(f"No data returned for {ticker}")
            continue

        # Handle possible MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data = data.xs(
                ticker,
                axis=1,
                level=1
            )

        # Extract raw and adjusted prices
        raw_close = data["Close"]
        adjusted_close = data["Adj Close"]

        # Calculate daily returns
        raw_returns = raw_close.pct_change(
            fill_method=None
        )

        adjusted_returns = adjusted_close.pct_change(
            fill_method=None
        )

        # Compare returns in basis points
        adjustment_impact = (
            adjusted_returns - raw_returns
        ) * 10000

        comparison = pd.DataFrame({
            "Raw Return (%)": raw_returns * 100,
            "Adjusted Return (%)":
                adjusted_returns * 100,
            "Adjustment Impact (bps)":
                adjustment_impact
        })

        print("\nRaw vs Adjusted Daily Returns:")
        print(
            comparison.round(4).to_string()
        )

        # Display dividend events if available
        if "Dividends" in data.columns:

            dividends = data["Dividends"]

            dividend_events = dividends[
                dividends > 0
            ]

            print("\nDividend Events:")
            print(dividend_events)

        # Display raw and adjusted prices
        print("\nClosing Prices:")
        print(
            data[["Close", "Adj Close"]]
            .round(4)
            .to_string()
        )


if __name__ == "__main__":
    main()
