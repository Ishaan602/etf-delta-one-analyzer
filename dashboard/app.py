
"""
ETF Delta One Analytics Platform

Interactive Streamlit dashboard for ETF performance,
market sensitivity, relative tracking error, and
volatility analysis.

Reference ETF: SPY
Assets: SPY, IVV, VOO
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATHS AND IMPORTS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data_loader import download_etf_data, ETF_TICKERS

from tracking_metrics import (
    calculate_daily_returns,
    calculate_cumulative_returns,
    calculate_tracking_error,
    calculate_beta,
    calculate_correlation,
    calculate_rolling_volatility,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ETF Delta One | Quantitative Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONSTANTS
# ============================================================

REFERENCE_ETF = "SPY"
ROLLING_WINDOW = 20
TRADING_DAYS = 252

PERIOD_OPTIONS = {
    "3 Months": 3,
    "6 Months": 6,
    "1 Year": 12,
}


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_market_data():
    """
    Download ETF prices and calculate daily and
    cumulative returns.

    Cached for one hour.
    """

    data = download_etf_data()

    closing_prices = pd.DataFrame({
        ticker: data[ticker]["Close"]
        for ticker in ETF_TICKERS
    })

    closing_prices = closing_prices.sort_index()

    if closing_prices.empty:
        raise ValueError("No ETF prices were downloaded.")

    if closing_prices.isna().any().any():
        raise ValueError(
            "Missing adjusted closing prices detected."
        )

    if (closing_prices <= 0).any().any():
        raise ValueError(
            "ETF closing prices must be positive."
        )

    if len(closing_prices) < ROLLING_WINDOW + 1:
        raise ValueError(
            "Insufficient history for rolling volatility."
        )

    daily_returns = calculate_daily_returns(
        closing_prices
    )

    cumulative_returns = calculate_cumulative_returns(
        daily_returns
    )

    return closing_prices, daily_returns, cumulative_returns


# ============================================================
# RISK CALCULATIONS
# ============================================================

def calculate_dashboard_risk(
    daily_returns,
    cumulative_returns,
):
    """
    Calculate all six quantitative risk report metrics.

    SPY is used as a peer reference ETF.
    """

    clean_returns = daily_returns.dropna()

    reference_returns = clean_returns[REFERENCE_ETF]

    rolling_volatility = calculate_rolling_volatility(
        clean_returns,
        window=ROLLING_WINDOW,
        trading_days=TRADING_DAYS,
    )

    results = []

    for ticker in ETF_TICKERS:

        etf_returns = clean_returns[ticker]

        beta = calculate_beta(
            etf_returns,
            reference_returns,
        )

        correlation = calculate_correlation(
            etf_returns,
            reference_returns,
        )

        tracking_error = calculate_tracking_error(
            etf_returns,
            reference_returns,
            trading_days=TRADING_DAYS,
        )

        cumulative_return = (
            cumulative_returns[ticker].iloc[-1] * 100
        )

        latest_volatility = (
            rolling_volatility[ticker].iloc[-1] * 100
        )

        average_volatility = (
            rolling_volatility[ticker].mean() * 100
        )

        results.append({
            "ETF": ticker,
            "Cumulative Return (%)": cumulative_return,
            "Beta vs SPY": beta,
            "Correlation vs SPY": correlation,
            "Relative Tracking Error (%)":
                tracking_error * 100,
            "20D Annualized Volatility (%)":
                latest_volatility,
            "Average 20D Volatility (%)":
                average_volatility,
        })

    report = pd.DataFrame(results).set_index("ETF")

    return report, rolling_volatility


# ============================================================
# VALIDATION
# ============================================================

def validate_risk_report(
    risk_summary,
    cumulative_returns,
):
    """Validate the consolidated risk report."""

    expected_columns = [
        "Cumulative Return (%)",
        "Beta vs SPY",
        "Correlation vs SPY",
        "Relative Tracking Error (%)",
        "20D Annualized Volatility (%)",
        "Average 20D Volatility (%)",
    ]

    assert list(risk_summary.columns) == expected_columns

    assert set(risk_summary.index) == set(ETF_TICKERS)

    assert np.isfinite(
        risk_summary.to_numpy(dtype=float)
    ).all()

    assert np.isclose(
        risk_summary.loc["SPY", "Beta vs SPY"],
        1.0,
    )

    assert np.isclose(
        risk_summary.loc["SPY", "Correlation vs SPY"],
        1.0,
    )

    assert np.isclose(
        risk_summary.loc[
            "SPY", "Relative Tracking Error (%)"
        ],
        0.0,
    )

    assert risk_summary[
        "Correlation vs SPY"
    ].between(-1.0 - 1e-10, 1.0 + 1e-10).all()

    for column in [
        "Relative Tracking Error (%)",
        "20D Annualized Volatility (%)",
        "Average 20D Volatility (%)",
    ]:
        assert (risk_summary[column] >= 0).all()

    expected_returns = (
        cumulative_returns.iloc[-1] * 100
    )

    actual_returns = risk_summary[
        "Cumulative Return (%)"
    ]

    assert np.allclose(
        actual_returns.loc[ETF_TICKERS].to_numpy(),
        expected_returns.loc[ETF_TICKERS].to_numpy(),
        rtol=1e-10,
        atol=1e-12,
    )


# ============================================================
# TABLE FORMATTING
# ============================================================

def format_risk_table(risk_summary):
    """Apply consistent financial number formatting."""

    return risk_summary.style.format({
        "Cumulative Return (%)": "{:.4f}%",
        "Beta vs SPY": "{:.6f}",
        "Correlation vs SPY": "{:.6f}",
        "Relative Tracking Error (%)": "{:.4f}%",
        "20D Annualized Volatility (%)": "{:.4f}%",
        "Average 20D Volatility (%)": "{:.4f}%",
    })


# ============================================================
# PAGE 1: MARKET OVERVIEW
# ============================================================

def show_market_overview(
    closing_prices,
    cumulative_returns,
    risk_summary,
):
    st.header("Market Overview")

    st.write(
        "Historical performance overview for "
        "SPY, IVV, and VOO."
    )

    latest_returns = (
        cumulative_returns.iloc[-1] * 100
    )

    st.subheader("ETF Cumulative Performance")

    columns = st.columns(3)

    for column, ticker in zip(columns, ETF_TICKERS):
        with column:
            st.metric(
                label=f"{ticker} Cumulative Return",
                value=f"{latest_returns[ticker]:.2f}%",
            )

    start_date = closing_prices.index[0].date()
    end_date = closing_prices.index[-1].date()

    st.caption(
        f"Observation period: {start_date} to {end_date}"
    )

    st.divider()

    st.subheader("Cumulative Performance Comparison")

    performance_pct = cumulative_returns * 100

    st.line_chart(
        performance_pct,
        x_label="Date",
        y_label="Cumulative Return (%)",
        height=420,
    )

    st.divider()

    st.subheader("Latest Adjusted Closing Prices")

    st.dataframe(
        closing_prices.tail(),
        use_container_width=True,
    )

    st.divider()

    st.subheader("Market Risk Snapshot")

    snapshot = risk_summary[
        [
            "20D Annualized Volatility (%)",
            "Relative Tracking Error (%)",
        ]
    ]

    st.dataframe(
        snapshot.style.format({
            "20D Annualized Volatility (%)": "{:.4f}%",
            "Relative Tracking Error (%)": "{:.4f}%",
        }),
        use_container_width=True,
    )

    st.caption(
        "Returns use dividend-adjusted historical prices. "
        "SPY is the peer reference for tracking metrics."
    )


# ============================================================
# PAGE 2: RISK ANALYTICS
# ============================================================

def show_risk_analytics(
    risk_summary,
    rolling_volatility,
):
    st.header("Risk Analytics")

    st.write(
        "Analyze market sensitivity, correlation, "
        "relative tracking error, and volatility."
    )

    st.subheader("Quantitative Risk Summary")

    st.dataframe(
        format_risk_table(risk_summary),
        use_container_width=True,
    )

    st.divider()

    selected_etf = st.selectbox(
        "Select an ETF to analyze",
        options=ETF_TICKERS,
        index=0,
        key="risk_etf_selector",
    )

    selected_risk = risk_summary.loc[selected_etf]

    st.subheader(f"{selected_etf} Risk Monitor")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Beta vs SPY",
            f"{selected_risk['Beta vs SPY']:.6f}",
        )

        st.metric(
            "Relative Tracking Error",
            (
                f"{selected_risk['Relative Tracking Error (%)']:.4f}%"
            ),
        )

    with col2:
        st.metric(
            "Correlation vs SPY",
            f"{selected_risk['Correlation vs SPY']:.6f}",
        )

        st.metric(
            "Latest 20-Day Volatility",
            (
                f"{selected_risk['20D Annualized Volatility (%)']:.4f}%"
            ),
        )

    st.divider()

    st.subheader(
        f"{selected_etf} Rolling Volatility"
    )

    selected_volatility = (
        rolling_volatility[selected_etf] * 100
    ).dropna()

    if selected_volatility.empty:
        st.warning("No rolling volatility data available.")
        return

    volatility_df = pd.DataFrame({
        "Annualized Volatility (%)":
            selected_volatility
    })

    st.line_chart(
        volatility_df,
        x_label="Date",
        y_label="Annualized Volatility (%)",
        height=420,
    )

    latest_volatility = selected_volatility.iloc[-1]
    peak_volatility = selected_volatility.max()
    peak_date = selected_volatility.idxmax()

    expected_volatility = risk_summary.loc[
        selected_etf,
        "20D Annualized Volatility (%)",
    ]

    assert np.isclose(
        latest_volatility,
        expected_volatility,
        rtol=1e-10,
        atol=1e-12,
    ), "Volatility chart validation failed."

    assert peak_volatility >= latest_volatility
    assert peak_date in selected_volatility.index
    assert selected_volatility.ge(0).all()

    vol_col1, vol_col2 = st.columns(2)

    with vol_col1:
        st.metric(
            "Latest 20-Day Volatility",
            f"{latest_volatility:.2f}%",
        )

    with vol_col2:
        st.metric(
            "Maximum 20-Day Volatility",
            f"{peak_volatility:.2f}%",
        )

    st.caption(
        f"Peak 20-day volatility: {peak_date.date()}. "
        "Annualized using 252 trading days."
    )

    st.info(
        "Relative tracking error is measured against "
        "SPY, not an official S&P 500 total-return index."
    )


# ============================================================
# PAGE 3: ETF COMPARISON
# ============================================================

def show_etf_comparison(
    closing_prices,
    cumulative_returns,
):
    st.header("ETF Comparison")

    st.write(
        "Compare the historical performance of "
        "multiple S&P 500 ETFs."
    )

    selected_etfs = st.multiselect(
        "Choose ETFs to compare",
        options=ETF_TICKERS,
        default=ETF_TICKERS,
        key="comparison_etfs",
    )

    selected_period = st.selectbox(
        "Select comparison period",
        options=list(PERIOD_OPTIONS.keys()),
        index=2,
        key="comparison_period",
    )

    if not selected_etfs:
        st.warning(
            "Please select at least one ETF to compare."
        )
        return

    months = PERIOD_OPTIONS[selected_period]

    end_date = closing_prices.index[-1]

    start_date = (
        end_date - pd.DateOffset(months=months)
    )

    period_prices = closing_prices.loc[
        closing_prices.index >= start_date,
        selected_etfs,
    ]

    if len(period_prices) < 2:
        st.warning(
            "Insufficient observations for the selected period."
        )
        return

    # Rebase performance to the selected starting price
    comparison_returns = (
        period_prices.div(period_prices.iloc[0]) - 1
    ) * 100

    # Validate that all selected ETFs begin at zero
    assert np.allclose(
        comparison_returns.iloc[0].to_numpy(
            dtype=float
        ),
        0.0,
        rtol=1e-10,
        atol=1e-12,
    )

    # Validate final returns
    expected_final = (
        period_prices.iloc[-1]
        / period_prices.iloc[0]
        - 1
    ) * 100

    actual_final = comparison_returns.iloc[-1]

    assert np.allclose(
        actual_final.to_numpy(dtype=float),
        expected_final.to_numpy(dtype=float),
        rtol=1e-10,
        atol=1e-12,
    )

    st.subheader("Cumulative Performance Comparison")

    st.line_chart(
        comparison_returns,
        x_label="Date",
        y_label="Cumulative Return (%)",
        height=450,
    )

    st.caption(
        f"Selected period: "
        f"{period_prices.index[0].date()} to "
        f"{period_prices.index[-1].date()}"
    )

    st.divider()

    st.subheader("Performance Ranking")

    final_returns = comparison_returns.iloc[-1]

    ranking = pd.DataFrame({
        "ETF": final_returns.index,
        "Cumulative Return (%)": final_returns.values,
    })

    ranking = ranking.sort_values(
        "Cumulative Return (%)",
        ascending=False,
    ).reset_index(drop=True)

    st.dataframe(
        ranking.style.format({
            "Cumulative Return (%)": "{:.4f}%"
        }),
        hide_index=True,
        use_container_width=True,
    )

    st.caption(
        "The selected period affects this comparison "
        "page only. The risk report uses the full "
        "downloaded observation period."
    )


# ============================================================
# PAGE 4: REPORTS
# ============================================================

def show_reports(
    risk_summary,
    closing_prices,
):
    st.header("Reports")

    st.write(
        "Review and export the consolidated "
        "six-metric ETF quantitative risk report."
    )

    st.subheader("Quantitative Risk Summary")

    st.dataframe(
        format_risk_table(risk_summary),
        use_container_width=True,
    )

    st.divider()

    st.subheader("Export Quantitative Risk Report")

    csv_data = risk_summary.to_csv(
        index=True,
        index_label="ETF",
        float_format="%.6f",
    )

    st.download_button(
        label="Download ETF Risk Report (CSV)",
        data=csv_data,
        file_name="etf_risk_report.csv",
        mime="text/csv",
        icon=":material/download:",
        key="risk_report_download",
    )

    st.caption(
        "The report contains cumulative return, beta, "
        "correlation, relative tracking error, latest "
        "20-day volatility, and average rolling volatility."
    )

    st.divider()

    st.subheader("Report Methodology")

    st.write(
        "**Reference ETF:** SPY"
    )

    st.write(
        "**Volatility window:** 20 trading days"
    )

    st.write(
        "**Annualization factor:** 252 trading days"
    )

    st.write(
        "**Price methodology:** Dividend-adjusted "
        "historical closing prices"
    )

    st.write(
        "**Data source:** Yahoo Finance via yfinance"
    )

    st.caption(
        "Observation period: "
        f"{closing_prices.index[0].date()} to "
        f"{closing_prices.index[-1].date()}"
    )

    st.warning(
        "This report is for educational and research "
        "purposes only. SPY is a peer reference ETF, "
        "not an official total-return benchmark. "
        "Historical estimates are not forecasts."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("ETF Delta One")

    st.caption("Quantitative Trading Analytics")

    st.divider()

    st.subheader("Dashboard Navigation")

    navigation = st.radio(
        "Navigate to",
        options=[
            "Market Overview",
            "Risk Analytics",
            "ETF Comparison",
            "Reports",
        ],
        index=0,
        key="main_navigation",
    )

    st.divider()

    st.subheader("Project Information")

    st.write("**Assets:** SPY, IVV, VOO")
    st.write("**Asset Class:** US Equities")
    st.write("**Reference ETF:** SPY")
    st.write("**Data Source:** Yahoo Finance")

    st.divider()

    st.caption(
        "Educational quantitative finance project. "
        "Not investment advice."
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    st.title("ETF Delta One Analytics Platform")

    st.markdown(
        """
        **Quantitative ETF Performance & Risk Monitoring**

        Analyze historical performance, market
        sensitivity, relative tracking error,
        and volatility across S&P 500 ETFs.
        """
    )

    st.caption(
        "Built with Python, Pandas, NumPy, "
        "yfinance, and Streamlit."
    )

    st.divider()

    # Load shared data
    try:
        with st.spinner("Loading ETF market data..."):
            (
                closing_prices,
                daily_returns,
                cumulative_returns,
            ) = load_market_data()

            (
                risk_summary,
                rolling_volatility,
            ) = calculate_dashboard_risk(
                daily_returns,
                cumulative_returns,
            )

            validate_risk_report(
                risk_summary,
                cumulative_returns,
            )

    except Exception as error:
        st.error("Unable to load or analyze ETF data.")
        st.exception(error)
        st.stop()

    # Display current dataset information
    st.caption(
        "Market data through "
        f"{closing_prices.index[-1].date()} "
        "| Cached for up to one hour"
    )

    # Route to the selected dashboard page
    if navigation == "Market Overview":

        show_market_overview(
            closing_prices,
            cumulative_returns,
            risk_summary,
        )

    elif navigation == "Risk Analytics":

        show_risk_analytics(
            risk_summary,
            rolling_volatility,
        )

    elif navigation == "ETF Comparison":

        show_etf_comparison(
            closing_prices,
            cumulative_returns,
        )

    elif navigation == "Reports":

        show_reports(
            risk_summary,
            closing_prices,
        )


if __name__ == "__main__":
    main()
