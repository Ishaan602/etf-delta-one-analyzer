
import yfinance as yf
import pandas as pd

TICKERS = ["SPY", "IVV", "VOO"]

START_DATE = "2026-06-15"
END_DATE = "2026-07-06"


def main():
    print("================================")
    print("ETF Dividend Event Investigation")
    print("================================")

    for ticker in TICKERS:
        print(f"\n--- {ticker} ---")

        # Download daily prices and corporate actions
        data = yf.Ticker(ticker).history(
            start=START_DATE,
            end=END_DATE,
            interval="1d",
            auto_adjust=False,
            actions=True
        )

        if data.empty:
            print("No data returned.")
            continue

        # Display recorded dividend events
        dividends = data.loc[
            data["Dividends"] != 0,
            ["Dividends"]
        ]

        print("\nDividend events:")
        if dividends.empty:
            print("No dividend events in this period.")
        else:
            print(dividends)

        # Calculate the historical adjustment factor
        data["Adjustment Factor"] = (
            data["Adj Close"] / data["Close"]
        )

        print("\nClosing prices and adjustment factors:")
        print(
            data[
                ["Close", "Adj Close", "Adjustment Factor"]
            ].round(6)
        )


if __name__ == "__main__":
    main()
