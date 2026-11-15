
import pandas as pd
import numpy as np

from tracking_metrics import calculate_tracking_error


def main():
    # Sample daily returns
    benchmark_returns = pd.Series(
        [0.010, -0.005, 0.008, 0.012, -0.003]
    )

    etf_returns = pd.Series(
        [0.011, -0.006, 0.009, 0.010, -0.002]
    )

    # Calculate tracking error
    tracking_error = calculate_tracking_error(
        etf_returns,
        benchmark_returns
    )

    print("Annualized Tracking Error:")
    print(f"{tracking_error * 100:.4f}%")

    # Independently calculate expected result
    differences = np.array([
        0.001, -0.001, 0.001, -0.002, 0.001
    ])

    expected = np.std(
        differences, ddof=1
    ) * np.sqrt(252)

    print("\nExpected Tracking Error:")
    print(f"{expected * 100:.4f}%")

    assert np.isclose(
        tracking_error,
        expected,
        rtol=1e-10,
        atol=1e-12
    ), "Tracking error validation failed!"

    print("\nTracking error validated successfully!")


if __name__ == "__main__":
    main()
