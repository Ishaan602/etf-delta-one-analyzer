
from pathlib import Path
import hashlib

import numpy as np
import pandas as pd


# ---------------------------------------
# EXPECTED BENCHMARK INFORMATION
# ---------------------------------------

EXPECTED_SHA256 = (
    "c0fdebd368dcc2bb5fc336699e771df6496d9ef2e56d24d54db2b23445f7a358"
)

EXPECTED_START = "2025-11-14"
EXPECTED_END = "2026-11-13"
EXPECTED_ROWS = 251
EXPECTED_RETURN = 13.5813


PROJECT_ROOT = Path(__file__).resolve().parent.parent

BENCHMARK_PATH = (
    PROJECT_ROOT
    / "data"
    / "sp500_total_return_2025-11-14_2026-11-13.csv"
)

ETF_PATH = (
    PROJECT_ROOT
    / "data"
    / "etf_adjusted_prices_2025-11-14_2026-11-13.csv"
)


def main():

    print("=" * 45)
    print("Saved S&P 500 Benchmark Validation")
    print("=" * 45)

    # 1. Verify both files exist
    if not BENCHMARK_PATH.is_file():
        raise FileNotFoundError(
            f"Benchmark not found: {BENCHMARK_PATH}"
        )

    if not ETF_PATH.is_file():
        raise FileNotFoundError(
            f"ETF snapshot not found: {ETF_PATH}"
        )

    # 2. Verify the benchmark checksum
    actual_sha256 = hashlib.sha256(
        BENCHMARK_PATH.read_bytes()
    ).hexdigest()

    assert actual_sha256 == EXPECTED_SHA256, (
        "Benchmark SHA-256 checksum mismatch!"
    )

    print("PASS: Benchmark checksum matches.")

    # 3. Read the saved benchmark CSV
    benchmark = pd.read_csv(
        BENCHMARK_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    # Validate expected columns
    assert list(benchmark.columns) == ["SP500TR"], (
        "Unexpected benchmark columns!"
    )

    print("PASS: Benchmark columns match.")

    # 4. Validate historical coverage
    assert len(benchmark) == EXPECTED_ROWS, (
        f"Expected {EXPECTED_ROWS} observations, "
        f"found {len(benchmark)}"
    )

    assert (
        benchmark.index[0].date().isoformat()
        == EXPECTED_START
    ), "Unexpected starting date!"

    assert (
        benchmark.index[-1].date().isoformat()
        == EXPECTED_END
    ), "Unexpected ending date!"

    print("PASS: Historical coverage matches.")

    # 5. Validate date index
    assert benchmark.index.is_unique, (
        "Duplicate benchmark dates detected!"
    )

    assert benchmark.index.is_monotonic_increasing, (
        "Benchmark dates are not sorted!"
    )

    assert (
        benchmark.index.dayofweek < 5
    ).all(), "Weekend dates detected!"

    print("PASS: Benchmark date index is valid.")

    # 6. Validate index levels
    levels = benchmark["SP500TR"]

    assert levels.notna().all(), (
        "Missing index levels detected!"
    )

    assert np.isfinite(
        levels.to_numpy(dtype=float)
    ).all(), "Non-finite index levels detected!"

    assert (levels > 0).all(), (
        "Nonpositive index levels detected!"
    )

    print("PASS: Index levels are finite and positive.")

    # 7. Verify alignment with ETF snapshot
    etf_prices = pd.read_csv(
        ETF_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    assert benchmark.index.equals(etf_prices.index), (
        "Benchmark dates do not match ETF dates!"
    )

    print("PASS: Benchmark and ETF dates match.")

    # 8. Calculate daily benchmark returns
    daily_returns = levels.pct_change(
        fill_method=None
    )

    assert pd.isna(daily_returns.iloc[0]), (
        "First daily return should be NaN!"
    )

    assert daily_returns.iloc[1:].notna().all(), (
        "Missing benchmark daily returns!"
    )

    assert np.isfinite(
        daily_returns.iloc[1:].to_numpy(dtype=float)
    ).all(), "Invalid daily benchmark returns!"

    print("PASS: Daily benchmark returns are valid.")

    # 9. Calculate cumulative benchmark return
    cumulative_return = (
        levels.iloc[-1] / levels.iloc[0] - 1
    ) * 100

    assert np.isclose(
        cumulative_return,
        EXPECTED_RETURN,
        atol=0.0001,
        rtol=0
    ), "Benchmark cumulative return mismatch!"

    print("PASS: Cumulative return matches.")

    # 10. Display results
    print("\nBenchmark Summary:")
    print(f"First date: {benchmark.index[0].date()}")
    print(f"Last date: {benchmark.index[-1].date()}")
    print(f"Observations: {len(benchmark)}")

    print(
        f"Cumulative Return: "
        f"{cumulative_return:.4f}%"
    )

    print("\nFirst 3 Index Levels:")
    print(benchmark.head(3))

    print("\nLast 3 Index Levels:")
    print(benchmark.tail(3))

    print("\nALL BENCHMARK VALIDATIONS PASSED!")


if __name__ == "__main__":
    main()
