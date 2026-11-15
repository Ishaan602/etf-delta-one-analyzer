
import pandas as pd
import numpy as np

from tracking_metrics import (
    calculate_rolling_volatility
)


def main():
    print("================================")
    print("Rolling Volatility Validation")
    print("================================")

    # Sample daily returns in decimal form
    sample_returns = pd.Series([
        0.010,
        -0.005,
        0.008,
        -0.012,
        0.006,
        0.015,
        -0.009
    ])

    # Calculate 5-day rolling volatility
    rolling_vol = calculate_rolling_volatility(
        sample_returns,
        window=5
    )

    print("\nRolling Volatility (%):")
    print((rolling_vol * 100).round(4))

    # Independently calculate the first
    # valid rolling volatility observation
    first_window = np.array([
        0.010,
        -0.005,
        0.008,
        -0.012,
        0.006
    ])

    expected = (
        np.std(first_window, ddof=1)
        * np.sqrt(252)
    )

    actual = rolling_vol.iloc[4]

    print("\nExpected First Volatility:")
    print(f"{expected * 100:.4f}%")

    print("\nCalculated First Volatility:")
    print(f"{actual * 100:.4f}%")

    # Check the first four values are NaN
    assert rolling_vol.iloc[:4].isna().all(), (
        "Initial rolling values should be NaN!"
    )

    # Check the first valid result
    assert np.isclose(
        actual,
        expected,
        rtol=1e-10,
        atol=1e-12
    ), "Rolling volatility validation failed!"

    # Verify the remaining rolling values
    for end in range(5, len(sample_returns) + 1):
        window_data = sample_returns.iloc[end-5:end]

        expected_value = (
            np.std(window_data.to_numpy(), ddof=1)
            * np.sqrt(252)
        )

        actual_value = rolling_vol.iloc[end-1]

        assert np.isclose(
            actual_value,
            expected_value,
            rtol=1e-10,
            atol=1e-12
        ), f"Validation failed at observation {end}!"

    print("\nRolling volatility validated successfully!")


if __name__ == "__main__":
    main()
