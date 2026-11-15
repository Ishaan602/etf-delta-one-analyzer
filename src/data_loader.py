
import yfinance as yf
import pandas as pd

# ETFs we want to analyze
ETF_TICKERS = ["SPY", "IVV", "VOO"]

# S&P 500 price index (for later comparison)
BENCHMARK = "^GSPC"


def download_etf_data():
    """
    Download one year of historical daily ETF prices.
    """

    print("Downloading historical ETF data...")

    data = yf.download(
        tickers=ETF_TICKERS,
        period="1y",
        interval="1d",
        auto_adjust=True,
        progress=False,
        group_by="ticker"
    )

    if data.empty:
        raise RuntimeError("No market data was downloaded.")

    return data


def main():
    print("================================")
    print("ETF Delta One Analytics Platform")
    print("================================")

    data = download_etf_data()

    print("\nDownload successful!")

    print("\nFirst 5 rows:")
    print(data.head())

    print("\nLast 5 rows:")
    print(data.tail())

    print("\nDataset dimensions:")
    print(data.shape)

    print("\nColumn structure:")
    print(data.columns)

    print("\nSPY closing prices:")
    print(data["SPY"]["Close"].head())
    print("\nMissing closing prices by ETF:")

    for ticker in ETF_TICKERS:
        missing = data[ticker]["Close"].isna().sum()
        print(f"{ticker}: {missing} missing values")    

if __name__ == "__main__":
    main()
