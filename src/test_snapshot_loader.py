
import numpy as np
import pandas as pd

from data_loader import (
    load_etf_data,
    download_etf_data,
    ETF_TICKERS
)


def main():
    print("================================")
    print("ETF Snapshot Loader Test")
    print("================================")

    # Load the saved snapshot
    data = load_etf_data(source="snapshot")

    # Extract adjusted closing prices
    prices = pd.DataFrame({
        ticker: data[ticker]["Close"]
        for ticker in ETF_TICKERS
    })

    print("\nDataset Summary:")
    print(f"First date: {prices.index[0].date()}")
    print(f"Last date: {prices.index[-1].date()}")
    print(f"Trading sessions: {len(prices)}")
    print(f"ETFs: {list(prices.columns)}")

    # Validate historical coverage
    assert len(prices) == 251
    assert prices.index[0].date().isoformat() == "2025-11-14"
    assert prices.index[-1].date().isoformat() == "2026-11-13"

    # Validate numerical prices
    assert np.isfinite(
        prices.to_numpy(dtype=float)
    ).all()

    assert (prices > 0).all().all()

    # Check backward compatibility
    legacy_data = download_etf_data()

    legacy_prices = pd.DataFrame({
        ticker: legacy_data[ticker]["Close"]
        for ticker in ETF_TICKERS
    })

    pd.testing.assert_frame_equal(
        prices,
        legacy_prices
    )

    print("\nSnapshot loader validated successfully!")
    print("Backward compatibility validated successfully!")


if __name__ == "__main__":
    main()
