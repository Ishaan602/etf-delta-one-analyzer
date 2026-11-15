
from pathlib import Path
import hashlib

import numpy as np
import pandas as pd


# Original snapshot fingerprint
EXPECTED_SHA256 = (
    "9b250ff036b9364fcc97ea773571baee68c8736fd0bfd7307deb1a847e346e09"
)

EXPECTED_TICKERS = ["SPY", "IVV", "VOO"]
EXPECTED_START = "2025-11-14"
EXPECTED_END = "2026-11-13"
EXPECTED_ROWS = 251


def main():
    print("================================")
    print("ETF Snapshot Validation")
    print("================================")

    # Locate the snapshot relative to this script
    project_root = Path(__file__).resolve().parent.parent

    snapshot_path = (
        project_root
        / "data"
        / "etf_adjusted_prices_2025-11-14_2026-11-13.csv"
    )

    # Check that the file exists
    if not snapshot_path.is_file():
        raise FileNotFoundError(
            f"Snapshot not found: {snapshot_path}"
        )

    # 1. Verify file integrity
    actual_sha256 = hashlib.sha256(
        snapshot_path.read_bytes()
    ).hexdigest()

    assert actual_sha256 == EXPECTED_SHA256, (
        "Snapshot checksum mismatch!"
    )

    print("PASS: SHA-256 checksum matches.")

    # 2. Read the saved CSV
    prices = pd.read_csv(
        snapshot_path,
        index_col="Date",
        parse_dates=["Date"]
    )

    # 3. Validate column structure
    assert list(prices.columns) == EXPECTED_TICKERS, (
        f"Unexpected ETF columns: {list(prices.columns)}"
    )

    print("PASS: ETF columns match.")

    # 4. Validate historical coverage
    assert len(prices) == EXPECTED_ROWS, (
        f"Expected {EXPECTED_ROWS} rows, "
        f"found {len(prices)}"
    )

    assert prices.index[0].date().isoformat() == EXPECTED_START
    assert prices.index[-1].date().isoformat() == EXPECTED_END

    print("PASS: Historical dates and row count match.")

    # 5. Validate the date index
    assert prices.index.is_unique, (
        "Duplicate trading dates detected!"
    )

    assert prices.index.is_monotonic_increasing, (
        "Trading dates are not sorted!"
    )

    assert prices.index.dayofweek.isin(
        [0, 1, 2, 3, 4]
    ).all(), "Weekend dates detected!"

    print("PASS: Trading-date index is valid.")

    # 6. Validate numerical prices
    assert prices.notna().all().all(), (
        "Missing price observations detected!"
    )

    numeric_prices = prices.to_numpy(dtype=float)

    assert np.isfinite(numeric_prices).all(), (
        "Non-finite prices detected!"
    )

    assert (numeric_prices > 0).all(), (
        "Nonpositive prices detected!"
    )

    print("PASS: All prices are finite and positive.")

    # 7. Display the validated dataset
    print("\nDataset Summary:")
    print(f"First date: {prices.index[0].date()}")
    print(f"Last date: {prices.index[-1].date()}")
    print(f"Trading sessions: {len(prices)}")
    print(f"Tickers: {list(prices.columns)}")

    print("\nFirst 3 rows:")
    print(prices.head(3))

    print("\nLast 3 rows:")
    print(prices.tail(3))

    print("\nALL SNAPSHOT VALIDATIONS PASSED!")


if __name__ == "__main__":
    main()
