
import pandas as pd
import numpy as np

from tracking_metrics import (
    calculate_beta,
    calculate_correlation
)


def main():
    print("================================")
    print("Beta and Correlation Validation")
    print("================================")

    # Example benchmark returns
    benchmark_returns = pd.Series(
        [0.01, -0.02, 0.03, -0.01, 0.02]
    )

    # ETF moves exactly 1.2x the benchmark
    etf_returns = benchmark_returns * 1.2

    # Calculate metrics
    beta = calculate_beta(
        etf_returns,
        benchmark_returns
    )

    correlation = calculate_correlation(
        etf_returns,
        benchmark_returns
    )

    print(f"\nCalculated Beta: {beta:.4f}")
    print(f"Calculated Correlation: {correlation:.4f}")

    # Validate against known expected values
    assert np.isclose(
        beta, 1.2, atol=1e-10
    ), "Beta validation failed!"

    assert np.isclose(
        correlation, 1.0, atol=1e-10
    ), "Correlation validation failed!"

    print("\nBeta validated successfully!")
    print("Correlation validated successfully!")


if __name__ == "__main__":
    main()
