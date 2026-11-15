
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    print("================================")
    print("ETF Risk Report Comparison")
    print("================================")

    # Locate project root
    project_root = Path(__file__).resolve().parent.parent

    # Define report paths
    standalone_path = (
        project_root / "outputs" / "etf_risk_report.csv"
    )

    dashboard_path = (
        project_root / "outputs" / "etf_dashboard_report.csv"
    )

    # Check both files exist
    for path in [standalone_path, dashboard_path]:
        if not path.is_file():
            raise FileNotFoundError(
                f"Report not found: {path}"
            )

    # Read the CSV files
    standalone = pd.read_csv(
        standalone_path,
        index_col=0
    )

    dashboard = pd.read_csv(
        dashboard_path,
        index_col=0
    )

    # Validate expected ETFs and columns
    expected_etfs = ["SPY", "IVV", "VOO"]

    expected_columns = [
        "Cumulative Return (%)",
        "Beta vs SPY",
        "Correlation vs SPY",
        "Relative Tracking Error (%)",
        "20D Annualized Volatility (%)",
        "Average 20D Volatility (%)"
    ]

    if set(standalone.index) != set(expected_etfs):
        raise ValueError(
            "Standalone report has unexpected ETFs."
        )

    if set(dashboard.index) != set(expected_etfs):
        raise ValueError(
            "Dashboard report has unexpected ETFs."
        )

    if set(standalone.columns) != set(expected_columns):
        raise ValueError(
            "Standalone report has unexpected columns."
        )

    if set(dashboard.columns) != set(expected_columns):
        raise ValueError(
            "Dashboard report has unexpected columns."
        )

    # Align rows and columns
    standalone = standalone.loc[
        expected_etfs, expected_columns
    ]

    dashboard = dashboard.loc[
        expected_etfs, expected_columns
    ]

    # Convert to numerical arrays
    standalone_values = standalone.to_numpy(
        dtype=float
    )

    dashboard_values = dashboard.to_numpy(
        dtype=float
    )

    # Check for missing or invalid values
    if not np.isfinite(standalone_values).all():
        raise ValueError(
            "Standalone report contains invalid values."
        )

    if not np.isfinite(dashboard_values).all():
        raise ValueError(
            "Dashboard report contains invalid values."
        )

    # Calculate absolute differences
    differences = np.abs(
        standalone_values - dashboard_values
    )

    max_difference = differences.max()

    # Compare within CSV precision tolerance
    match = np.allclose(
        standalone_values,
        dashboard_values,
        rtol=0,
        atol=1e-6
    )

    print("\nStandalone Report:")
    print(standalone.round(6).to_string())

    print("\nDashboard Report:")
    print(dashboard.round(6).to_string())

    print("\nMaximum Absolute Difference:")
    print(f"{max_difference:.10f}")

    if not match:
        difference_table = pd.DataFrame(
            differences,
            index=expected_etfs,
            columns=expected_columns
        )

        print("\nAbsolute Differences:")
        print(difference_table.to_string())

        raise AssertionError(
            "Risk reports do not match!"
        )

    print("\nPASS: All six risk metrics match!")
    print("PASS: Dashboard and standalone reports agree!")


if __name__ == "__main__":
    main()
