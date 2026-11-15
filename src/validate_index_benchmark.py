
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


BENCHMARK = "^SP500TR"
START_DATE = "2025-11-14"
END_DATE = "2026-11-14"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SNAPSHOT_PATH = (
    PROJECT_ROOT
    / "data"
    / "etf_adjusted_prices_2025-11-14_2026-11-13.csv"
)


def main():
    print("=" * 45)
    print("S&P 500 Benchmark Validation")
    print("=" * 45)

    # 1. Load the existing ETF snapshot
    etf_prices = pd.read_csv(
        SNAPSHOT_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    # 2. Download the total-return index
    benchmark_data = yf.download(
        BENCHMARK,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=False
    )

    if benchmark_data.empty:
        raise ValueError(
            "No benchmark data returned."
        )

    # 3. Extract benchmark closing levels
    if isinstance(
        benchmark_data.columns,
        pd.MultiIndex
    ):
        benchmark_prices = (
            benchmark_data["Close"].iloc[:, 0]
        )
    else:
        benchmark_prices = benchmark_data["Close"]

    benchmark_prices.name = "SP500TR"

    # 4. Normalize dates for comparison
    etf_prices.index = pd.to_datetime(
        etf_prices.index
    ).normalize()

    benchmark_prices.index = pd.to_datetime(
        benchmark_prices.index
    )

    if benchmark_prices.index.tz is not None:
        benchmark_prices.index = (
            benchmark_prices.index.tz_localize(None)
        )

    benchmark_prices.index = (
        benchmark_prices.index.normalize()
    )

    # 5. Check for duplicate dates
    assert etf_prices.index.is_unique, (
        "Duplicate ETF dates detected!"
    )

    assert benchmark_prices.index.is_unique, (
        "Duplicate benchmark dates detected!"
    )

    # 6. Compare exact trading dates
    missing_from_benchmark = (
        etf_prices.index.difference(
            benchmark_prices.index
        )
    )

    extra_benchmark_dates = (
        benchmark_prices.index.difference(
            etf_prices.index
        )
    )

    print("\nETF observations:", len(etf_prices))
    print(
        "Benchmark observations:",
        len(benchmark_prices)
    )

    print(
        "Missing benchmark dates:",
        len(missing_from_benchmark)
    )

    print(
        "Extra benchmark dates:",
        len(extra_benchmark_dates)
    )

    if len(missing_from_benchmark) > 0:
        print("\nMissing dates:")
        print(missing_from_benchmark)

    if len(extra_benchmark_dates) > 0:
        print("\nExtra dates:")
        print(extra_benchmark_dates)

    assert len(missing_from_benchmark) == 0, (
        "Benchmark is missing ETF trading dates!"
    )

    assert len(extra_benchmark_dates) == 0, (
        "Benchmark contains unexpected dates!"
    )

    print("\nPASS: Trading dates match exactly!")

    # 7. Align benchmark to ETF dates
    benchmark_prices = benchmark_prices.reindex(
        etf_prices.index
    )

    # 8. Validate benchmark levels
    assert benchmark_prices.notna().all(), (
        "Missing benchmark levels detected!"
    )

    assert np.isfinite(
        benchmark_prices.to_numpy(dtype=float)
    ).all(), "Non-finite benchmark levels detected!"

    assert (benchmark_prices > 0).all(), (
        "Nonpositive benchmark levels detected!"
    )

    print("PASS: Benchmark levels are valid!")

    # 9. Calculate daily benchmark returns
    benchmark_returns = benchmark_prices.pct_change(
        fill_method=None
    )

    assert pd.isna(benchmark_returns.iloc[0]), (
        "First return should be undefined!"
    )

    assert benchmark_returns.iloc[1:].notna().all(), (
        "Missing daily benchmark returns!"
    )

    assert np.isfinite(
        benchmark_returns.iloc[1:].to_numpy(
            dtype=float
        )
    ).all(), "Invalid benchmark returns!"

    print("PASS: Daily returns calculated!")

    # 10. Display benchmark information
    print("\nBenchmark Summary:")
    print("Symbol:", BENCHMARK)
    print(
        "First date:",
        benchmark_prices.index[0].date()
    )
    print(
        "Last date:",
        benchmark_prices.index[-1].date()
    )

    print("\nFirst 3 Index Levels:")
    print(benchmark_prices.head(3))

    print("\nLast 3 Index Levels:")
    print(benchmark_prices.tail(3))

    print("\nFirst 5 Valid Daily Returns (%):")
    print(
        (benchmark_returns.dropna().head() * 100)
        .round(4)
    )

    # 11. Calculate full-period benchmark return
    total_return = (
        benchmark_prices.iloc[-1]
        / benchmark_prices.iloc[0]
        - 1
    ) * 100

    print(
        "\nBenchmark Cumulative Return:",
        f"{total_return:.4f}%"
    )

    print("\nALL NUMERICAL VALIDATIONS PASSED!")


if __name__ == "__main__":
    main()
