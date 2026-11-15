
from pathlib import Path
import hashlib

import numpy as np
import pandas as pd
import yfinance as yf


# ---------------------------------------
# BENCHMARK CONFIGURATION
# ---------------------------------------

BENCHMARK = "^SP500TR"

START_DATE = "2025-11-14"
END_DATE = "2026-11-14"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ETF_SNAPSHOT = (
    PROJECT_ROOT
    / "data"
    / "etf_adjusted_prices_2025-11-14_2026-11-13.csv"
)

BENCHMARK_SNAPSHOT = (
    PROJECT_ROOT
    / "data"
    / "sp500_total_return_2025-11-14_2026-11-13.csv"
)


def main():

    print("=" * 45)
    print("S&P 500 Total Return Snapshot")
    print("=" * 45)

    # 1. Protect any existing benchmark snapshot
    if BENCHMARK_SNAPSHOT.exists():
        raise FileExistsError(
            f"Benchmark snapshot already exists: "
            f"{BENCHMARK_SNAPSHOT}"
        )

    # 2. Load existing ETF dates for alignment
    etf_prices = pd.read_csv(
        ETF_SNAPSHOT,
        index_col="Date",
        parse_dates=["Date"]
    )

    # 3. Download benchmark levels
    print("\nDownloading total-return index levels...")

    data = yf.download(
        BENCHMARK,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        raise ValueError(
            "No benchmark data returned."
        )

    # 4. Extract closing index levels
    if isinstance(data.columns, pd.MultiIndex):
        index_levels = data["Close"].iloc[:, 0]
    else:
        index_levels = data["Close"]

    index_levels = index_levels.copy()
    index_levels.name = "SP500TR"

    # 5. Normalize date indexes
    etf_dates = pd.to_datetime(etf_prices.index)

    benchmark_dates = pd.to_datetime(
        index_levels.index
    )

    if benchmark_dates.tz is not None:
        benchmark_dates = (
            benchmark_dates.tz_localize(None)
        )

    etf_dates = etf_dates.normalize()
    benchmark_dates = benchmark_dates.normalize()

    index_levels.index = benchmark_dates

    # 6. Validate dates and observations
    assert etf_dates.is_unique
    assert benchmark_dates.is_unique

    assert etf_dates.equals(benchmark_dates), (
        "Benchmark dates do not match ETF snapshot!"
    )

    assert len(index_levels) == 251, (
        "Unexpected benchmark observation count!"
    )

    # 7. Validate numerical index levels
    assert index_levels.notna().all(), (
        "Missing benchmark levels detected!"
    )

    assert np.isfinite(
        index_levels.to_numpy(dtype=float)
    ).all(), "Non-finite benchmark levels detected!"

    assert (index_levels > 0).all(), (
        "Nonpositive benchmark levels detected!"
    )

    # 8. Calculate cumulative return
    cumulative_return = (
        index_levels.iloc[-1]
        / index_levels.iloc[0]
        - 1
    ) * 100

    print(
        "\nBenchmark cumulative return:",
        f"{cumulative_return:.4f}%"
    )

    # Check consistency with previously observed result
    assert np.isclose(
        cumulative_return,
        13.5813,
        atol=0.01
    ), (
        "Benchmark return differs materially "
        "from the previously validated result!"
    )

    # 9. Save snapshot
    BENCHMARK_SNAPSHOT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    snapshot = pd.DataFrame({
        "SP500TR": index_levels
    })

    snapshot.to_csv(
        BENCHMARK_SNAPSHOT,
        index_label="Date",
        float_format="%.12f"
    )

    # 10. Calculate file checksum
    checksum = hashlib.sha256(
        BENCHMARK_SNAPSHOT.read_bytes()
    ).hexdigest()

    print("\nSnapshot saved successfully!")
    print(f"File: {BENCHMARK_SNAPSHOT}")

    print("\nSnapshot Summary:")
    print(f"First date: {snapshot.index[0].date()}")
    print(f"Last date: {snapshot.index[-1].date()}")
    print(f"Observations: {len(snapshot)}")

    print("\nSHA-256 Checksum:")
    print(checksum)

    print("\nFirst 3 Index Levels:")
    print(snapshot.head(3))

    print("\nLast 3 Index Levels:")
    print(snapshot.tail(3))


if __name__ == "__main__":
    main()
