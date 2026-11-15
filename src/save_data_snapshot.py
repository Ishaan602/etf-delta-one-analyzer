
from pathlib import Path
import hashlib

import pandas as pd

from data_loader import download_etf_data, ETF_TICKERS


def main():
    print("================================")
    print("ETF Historical Data Snapshot")
    print("================================")

    # Download the fixed historical dataset
    data = download_etf_data()

    # Extract adjusted closing prices
    prices = pd.DataFrame({
        ticker: data[ticker]["Close"]
        for ticker in ETF_TICKERS
    })

    prices = prices.sort_index()

    # Validate the dataset
    if prices.empty:
        raise ValueError("Dataset is empty!")

    if prices.isna().any().any():
        raise ValueError("Missing prices detected!")

    if (prices <= 0).any().any():
        raise ValueError("Invalid nonpositive prices!")

    if len(prices) != 251:
        raise ValueError(
            f"Expected 251 sessions, found {len(prices)}"
        )

    if prices.index[0].date().isoformat() != "2025-11-14":
        raise ValueError("Unexpected starting date!")

    if prices.index[-1].date().isoformat() != "2026-11-13":
        raise ValueError("Unexpected ending date!")

    # Create the data folder
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    # Define the snapshot filename
    output_file = (
        data_dir
        / "etf_adjusted_prices_2025-11-14_2026-11-13.csv"
    )

    # Avoid accidentally overwriting an existing snapshot
    if output_file.exists():
        raise FileExistsError(
            f"Snapshot already exists: {output_file}"
        )

    # Save adjusted closing prices
    prices.to_csv(
        output_file,
        index_label="Date",
        float_format="%.12f"
    )

    # Calculate SHA-256 checksum
    file_bytes = output_file.read_bytes()
    checksum = hashlib.sha256(file_bytes).hexdigest()

    print("\nSnapshot saved successfully!")
    print(f"File: {output_file}")

    print("\nDataset Summary:")
    print(f"First date: {prices.index[0].date()}")
    print(f"Last date: {prices.index[-1].date()}")
    print(f"Trading sessions: {len(prices)}")
    print(f"ETFs: {list(prices.columns)}")

    print("\nSHA-256 Checksum:")
    print(checksum)


if __name__ == "__main__":
    main()
