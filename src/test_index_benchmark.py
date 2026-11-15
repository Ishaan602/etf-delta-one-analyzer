
import pandas as pd
import yfinance as yf

BENCHMARK = "^SP500TR"

START_DATE = "2025-11-14"
END_DATE = "2026-11-14"


def main():
    print("=" * 45)
    print("S&P 500 Total Return Benchmark Test")
    print("=" * 45)

    print(f"\nRequesting: {BENCHMARK}")

    data = yf.download(
        BENCHMARK,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        print("\nNo benchmark data returned.")
        print("We need to investigate another source.")
        return

    # Handle possible yfinance MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"].iloc[:, 0]
    else:
        prices = data["Close"]

    prices = prices.dropna()

    if prices.empty:
        print("No valid closing levels returned.")
        return

    print("\nBenchmark Information:")
    print(f"Symbol: {BENCHMARK}")
    print(f"First date: {prices.index[0].date()}")
    print(f"Last date: {prices.index[-1].date()}")
    print(f"Observations: {len(prices)}")

    print("\nFirst 5 Index Levels:")
    print(prices.head())

    print("\nLast 5 Index Levels:")
    print(prices.tail())

    print("\nMissing values:", prices.isna().sum())

    # Inspect coverage without assuming it is complete
    if len(prices) == 251:
        print("\nObservation count matches ETF snapshot.")
    else:
        print("\nObservation count differs from ETF snapshot.")
        print("We will investigate date alignment.")


if __name__ == "__main__":
    main()
