
import pandas as pd

from pathlib import Path

from data_loader import download_etf_data, ETF_TICKERS

from tracking_metrics import (
    calculate_daily_returns,
    calculate_cumulative_returns,
    calculate_tracking_error,
    calculate_beta,
    calculate_correlation,
    calculate_rolling_volatility
)


def generate_risk_report():
    print("================================")
    print("ETF Quantitative Risk Report")
    print("================================")

    # Step 1: Download ETF data once
    data = download_etf_data()

    # Step 2: Extract adjusted closing prices
    closing_prices = pd.DataFrame({
        ticker: data[ticker]["Close"]
        for ticker in ETF_TICKERS
    })

    # Step 3: Validate the dataset
    if closing_prices.isna().any().any():
        raise ValueError(
            "Missing closing prices detected."
        )

    if len(closing_prices) < 22:
        raise ValueError(
            "Not enough observations for 20-day volatility."
        )

    # Step 4: Calculate daily returns
    daily_returns = calculate_daily_returns(
        closing_prices
    ).dropna()

    # Step 5: Calculate cumulative returns
    cumulative_returns = calculate_cumulative_returns(
        daily_returns
    )

    # Step 6: Calculate rolling volatility
    rolling_volatility = calculate_rolling_volatility(
        daily_returns,
        window=20
    )

    # Step 7: Use SPY as reference
    reference_returns = daily_returns["SPY"]

    # Step 8: Build report for each ETF
    results = []

    for ticker in ETF_TICKERS:

        etf_returns = daily_returns[ticker]

        # Cumulative performance
        total_return = (
            cumulative_returns[ticker].iloc[-1] * 100
        )

        # Market sensitivity
        beta = calculate_beta(
            etf_returns,
            reference_returns
        )

        # Correlation
        correlation = calculate_correlation(
            etf_returns,
            reference_returns
        )

        # Relative tracking error
        tracking_error = calculate_tracking_error(
            etf_returns,
            reference_returns
        ) * 100

        # Latest rolling volatility
        latest_volatility = (
            rolling_volatility[ticker].iloc[-1] * 100
        )

        # Average rolling volatility
        average_volatility = (
            rolling_volatility[ticker].mean() * 100
        )

        results.append({
            "ETF": ticker,
            "Cumulative Return (%)": total_return,
            "Beta vs SPY": beta,
            "Correlation vs SPY": correlation,
            "Relative Tracking Error (%)": tracking_error,
            "Latest 20D Volatility (%)": latest_volatility,
            "Average 20D Volatility (%)": average_volatility
        })

    # Step 9: Create report DataFrame
    report = pd.DataFrame(results)
    report = report.set_index("ETF")

    # ---------------------------------------
    # REPORT VALIDATION
    # ---------------------------------------

    import numpy as np

    # Check that all expected ETFs are present
    assert set(report.index) == set(ETF_TICKERS), (
        "Missing or unexpected ETFs in report!"
    )

    # Check that all report values are finite
    assert np.isfinite(
        report.to_numpy(dtype=float)
    ).all(), "Report contains invalid numeric values!"

    # SPY should have beta = 1 relative to itself
    assert np.isclose(
        report.loc["SPY", "Beta vs SPY"],
        1.0,
        atol=1e-10
    ), "SPY beta validation failed!"

    # SPY should have correlation = 1 with itself
    assert np.isclose(
        report.loc["SPY", "Correlation vs SPY"],
        1.0,
        atol=1e-10
    ), "SPY correlation validation failed!"

    # SPY tracking error relative to itself is zero
    assert np.isclose(
        report.loc["SPY", "Relative Tracking Error (%)"],
        0.0,
        atol=1e-10
    ), "SPY tracking error validation failed!"

    # Correlation must be between -1 and 1
    assert (
        report["Correlation vs SPY"]
        .between(-1.0 - 1e-10, 1.0 + 1e-10)
        .all()
    ), "Invalid correlation detected!"

    # Volatility and tracking error cannot be negative
    for column in [
        "Relative Tracking Error (%)",
        "Latest 20D Volatility (%)",
        "Average 20D Volatility (%)"
    ]:
        assert (report[column] >= 0).all(), (
            f"Negative risk metric detected: {column}"
        )

    print("\nAll risk report validation checks passed!")

    # Step 10: Display results
    print("\nObservation Period:")
    print(
        f"{closing_prices.index[0].date()} to "
        f"{closing_prices.index[-1].date()}"
    )

    print("\nQuantitative Risk Summary:")
    print(report.round(4).to_string())

    # Step 11: Save report as CSV
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "etf_risk_report.csv"

    report.round(6).to_csv(output_file)

    print(f"\nReport saved to: {output_file}")

    return report


if __name__ == "__main__":
    generate_risk_report()
