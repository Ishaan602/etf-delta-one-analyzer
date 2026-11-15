import yfinance as yf
import pandas as pd


# ETFs we will analyze
ETF_TICKERS = ["SPY", "IVV", "VOO"]

# Reference index
BENCHMARK = "^GSPC"


def main():
    print("================================")
    print("ETF Delta One Analytics Platform")
    print("================================")

    print("\nETFs to analyze:")
    for ticker in ETF_TICKERS:
        print(f" - {ticker}")

    print(f"\nBenchmark: {BENCHMARK}")

    print("\nData loader initialized successfully!")


if __name__ == "__main__":
    main()