
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ETF_PATH = (
    PROJECT_ROOT
    / "data"
    / "etf_adjusted_prices_2025-11-14_2026-11-13.csv"
)

INDEX_PATH = (
    PROJECT_ROOT
    / "data"
    / "sp500_total_return_2025-11-14_2026-11-13.csv"
)

EXPECTED_COLUMNS = ["SPY", "IVV", "VOO", "SP500TR"]


def main():
    print("=" * 45)
    print("ETF and Index Return Preparation")
    print("=" * 45)

    # 1. Load saved ETF prices
    etf_prices = pd.read_csv(
        ETF_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    # 2. Load saved total-return index levels
    index_prices = pd.read_csv(
        INDEX_PATH,
        index_col="Date",
        parse_dates=["Date"]
    )

    # 3. Verify the expected columns
    assert list(etf_prices.columns) == [
        "SPY", "IVV", "VOO"
    ], "Unexpected ETF columns!"

    assert list(index_prices.columns) == [
        "SP500TR"
    ], "Unexpected benchmark column!"

    # 4. Verify exact date alignment
    assert etf_prices.index.equals(
        index_prices.index
    ), "ETF and index dates do not match!"

    # 5. Combine into one DataFrame
    combined_prices = pd.concat(
        [etf_prices, index_prices],
        axis=1
    )

    # 6. Validate the combined prices
    assert list(combined_prices.columns) == (
        EXPECTED_COLUMNS
    ), "Unexpected combined columns!"

    assert len(combined_prices) == 251, (
        "Expected 251 price observations!"
    )

    assert combined_prices.index.is_unique, (
        "Duplicate dates detected!"
    )

    assert combined_prices.notna().all().all(), (
        "Missing prices detected!"
    )

    assert np.isfinite(
        combined_prices.to_numpy(dtype=float)
    ).all(), "Invalid prices detected!"

    assert (
        combined_prices > 0
    ).all().all(), "Nonpositive prices detected!"

    print("\nPASS: Combined prices validated!")

    # 7. Calculate daily returns
    daily_returns = combined_prices.pct_change(
        fill_method=None
    ).iloc[1:]

    # 8. Validate daily returns
    assert len(daily_returns) == 250, (
        "Expected 250 daily return observations!"
    )

    assert daily_returns.notna().all().all(), (
        "Missing daily returns detected!"
    )

    assert np.isfinite(
        daily_returns.to_numpy(dtype=float)
    ).all(), "Invalid daily returns detected!"

    print("PASS: Daily returns validated!")

    # 9. Verify ETF and index return dates
    assert daily_returns.index.equals(
        combined_prices.index[1:]
    ), "Return dates are misaligned!"

    print("PASS: Return dates aligned!")

    # 10. Display dataset information
    print("\nDataset Summary:")
    print(f"Price observations: {len(combined_prices)}")
    print(f"Return observations: {len(daily_returns)}")

    print(
        f"First return date: "
        f"{daily_returns.index[0].date()}"
    )

    print(
        f"Last return date: "
        f"{daily_returns.index[-1].date()}"
    )

    print("\nFirst 5 Daily Returns (%):")
    print(
        (daily_returns.head() * 100).round(4)
    )

    print("\nLast 5 Daily Returns (%):")
    print(
        (daily_returns.tail() * 100).round(4)
    )

    # 11. Validate cumulative returns against
    # first-to-last saved price levels
    cumulative_from_returns = (
        (1 + daily_returns).prod() - 1
    ) * 100

    cumulative_from_prices = (
        combined_prices.iloc[-1]
        / combined_prices.iloc[0]
        - 1
    ) * 100

    assert np.allclose(
        cumulative_from_returns.to_numpy(),
        cumulative_from_prices.to_numpy(),
        rtol=1e-10,
        atol=1e-10
    ), "Cumulative return validation failed!"

    print("\nCumulative Returns (%):")
    print(cumulative_from_returns.round(4))

    print("\nPASS: Cumulative returns validated!")
    print("\nALL RETURN PREPARATION CHECKS PASSED!")


if __name__ == "__main__":
    main()
