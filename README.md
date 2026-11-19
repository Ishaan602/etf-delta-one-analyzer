# ETF Delta One Analytics Platform

## Overview

A Python-based quantitative finance project designed to analyze the performance and risk characteristics of S&P 500 exchange-traded funds (ETFs).

The project explores quantitative concepts relevant to Delta One trading, including ETF index tracking, statistical risk analysis, and automated financial reporting.

## Project Objectives

- Download historical market data for SPY, IVV, and VOO.
- Compare ETF performance against an appropriate S&P 500 benchmark.
- Calculate tracking error, beta, correlation, and rolling volatility.
- Identify unusual ETF tracking deviations.
- Develop an interactive financial analytics dashboard using Streamlit.
- Explore simplified equity derivatives pricing.

## Technologies

Python | Pandas | NumPy | yfinance | Matplotlib | Streamlit | Jupyter

## Project Structure

- `src/` — Python scripts for data collection and financial calculations.
- `data/` — Historical market datasets.
- `notebooks/` — Exploratory quantitative analysis.
- `dashboard/` — Interactive Streamlit application.
- `outputs/` — Generated reports and visualizations.

## Getting Started

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the initial data loader:

```bash
python src/data_loader.py
```
### Generate the Quantitative Risk Report

Run the consolidated ETF risk analysis:

```bash
python src/generate_risk_report.py
```

The script downloads historical market data, calculates financial risk metrics, performs validation checks, and generates a CSV report.

The report is saved to:

`outputs/etf_risk_report.csv`

### Generate Performance and Risk Visualizations

Cumulative ETF performance:

```bash
python src/visualize_returns.py
```

20-day rolling annualized volatility:

```bash
python src/visualize_volatility.py
```

Generated charts are saved in the `outputs/` directory.

### Run Quantitative Validation Tests

```bash
python src/test_tracking_error.py
python src/test_beta_correlation.py
python src/test_rolling_volatility.py
```

These scripts verify the numerical implementation of tracking error, beta, correlation, and rolling volatility against controlled test cases.
## Current Status

## Project Status

**Phase 3 Complete — Quantitative Risk Analytics**

The project currently includes a functioning Python-based ETF analytics pipeline with historical market data retrieval, financial return calculations, quantitative risk metrics, validation checks, and automated reporting.

### Completed Features

- Historical market data collection for SPY, IVV, and VOO using yfinance.
- Daily and cumulative return calculations using Pandas and NumPy.
- Annualized relative tracking error calculations using SPY as the reference ETF.
- Beta and Pearson correlation analysis.
- 20-day rolling annualized volatility calculations.
- Investigation of tracking outliers, dividend adjustments, and short-term return reversals.
- Automated ETF risk summary reporting to CSV.
- Mathematical consistency checks for the core quantitative calculations.
- Historical performance and rolling volatility visualizations using Matplotlib.

### Quantitative Risk Summary

The following results were calculated using approximately one year of historical dividend-adjusted ETF prices ending November 13, 2026.

| Metric | SPY | IVV | VOO |
|---|---:|---:|---:|
| Cumulative Return (%) | 13.4804 | 13.5203 | 13.5211 |
| Beta vs. SPY | 1.0000 | 1.0006 | 0.9950 |
| Correlation vs. SPY | 1.0000 | 0.9992 | 0.9996 |
| Relative Tracking Error (%) | 0.0000 | 0.5364 | 0.3853 |
| Latest 20-Day Volatility (%) | 22.0719 | 22.0434 | 21.8920 |
| Average 20-Day Volatility (%) | 12.6038 | 12.6310 | 12.5569 |

### Key Findings

**Market Exposure:** All three ETFs exhibited highly similar market exposure, with IVV and VOO showing betas close to 1 and correlations above 0.999 relative to SPY.

**Tracking Consistency:** VOO exhibited lower annualized relative tracking error than IVV during the observation period.

**Outlier Sensitivity:** Removing five trading days between June 25 and July 1, 2026 reduced estimated relative tracking error by 35.63% for IVV and 28.52% for VOO.

**Short-Term Reversals:** Daily relative return differences frequently changed direction. The reversal pattern persisted after excluding the late-June outlier period.

**Changing Market Risk:** All three ETFs reached their highest observed 20-day annualized volatility on November 11, 2026. SPY's peak was approximately 22.38%, compared with an average rolling volatility of approximately 12.60%.

### Methodology and Limitations

- SPY is used as a peer reference ETF rather than an official S&P 500 total-return benchmark.
- Tracking-error estimates measure relative ETF return variability, not formal index replication accuracy.
- Historical adjusted-price data approximates total-return performance but may differ from official fund total-return calculations.
- The data is currently downloaded using a rolling one-year window. A fixed historical dataset will be introduced to improve reproducibility.
- Statistical relationships do not establish causality or profitable trading opportunities.

### Next Development Phase

## Phase 4 — Interactive Streamlit Dashboard

**Status: Complete**

Developed a four-page interactive quantitative finance dashboard using Streamlit, integrating historical ETF market data with reusable Python risk analytics functions.

### Dashboard Features

- **Market Overview:** Historical cumulative returns, adjusted closing prices, and a market risk snapshot for SPY, IVV, and VOO.
- **Risk Analytics:** Interactive ETF selection, beta, correlation, relative tracking error, and 20-day annualized rolling volatility.
- **ETF Comparison:** Multi-ETF performance comparisons, selectable 3-month, 6-month, and 1-year periods, and cumulative-return rankings.
- **Reports:** Consolidated six-metric quantitative risk report with downloadable CSV export.

### Technical Implementation

- Built using Python, Streamlit, Pandas, NumPy, Matplotlib, and yfinance.
- Reused validated financial calculations across the application.
- Implemented cached market data retrieval to reduce redundant downloads.
- Added automated consistency checks for financial metrics and performance calculations.
- Organized the dashboard into modular page functions with shared data processing.

### Run the Dashboard

From the project root directory:

```bash
python -m streamlit run dashboard/app.py
```

Open the local URL displayed in the Terminal, typically `http://localhost:8501`.

### Methodology Notes

The dashboard uses dividend-adjusted historical ETF prices. SPY serves as the reference ETF for relative beta, correlation, and tracking-error analysis.

The 3-month, 6-month, and 1-year controls affect the ETF Comparison page. The consolidated risk report uses the full downloaded observation period.

Historical results are descriptive and do not establish profitable trading opportunities or predict future performance.
### Interpretation

The results suggest that daily return differences between ETFs tracking the same index frequently reverse over short horizons. This pattern is consistent with temporary relative-price fluctuations, although additional data would be required to establish the underlying cause.

These findings are descriptive and do not demonstrate a profitable trading strategy. Further analysis of historical NAVs, market microstructure, and transaction costs would be necessary.

**Methodology note:** SPY was used as a peer reference ETF, not as an official S&P 500 total-return benchmark. Results are based on historical adjusted-price data and should be interpreted as relative ETF tracking analysis.

## Disclaimer

This project is intended for educational and portfolio purposes only and does not constitute investment advice.
## Reproducible Historical Market Data

The project supports reproducible ETF analysis using a versioned historical data snapshot.

### Historical Dataset

- **Assets:** SPY, IVV, VOO
- **Observation period:** November 14, 2025 – November 13, 2026
- **Trading sessions:** 251
- **Data source:** Yahoo Finance via yfinance
- **Price methodology:** Dividend-adjusted closing prices
- **Storage format:** CSV

The historical dataset is stored at:

`data/etf_adjusted_prices_2025-11-14_2026-11-13.csv`

### Data Integrity

The saved dataset was validated for expected ETF columns, historical coverage, duplicate dates, missing observations, finite positive prices, and file integrity.

The SHA-256 checksum of the saved snapshot is:

`9b250ff036b9364fcc97ea773571baee68c8736fd0bfd7307deb1a847e346e09`

### Data Loading

The analytics pipeline supports two data sources:

- **Snapshot mode (default):** Loads the saved historical CSV without downloading prices.
- **Yahoo Finance mode:** Downloads historical data using the configured fixed date range.

Snapshot mode is used by default to preserve consistent input data across repeated analyses.

### Reproducibility Validation

The standalone risk report and Streamlit dashboard were independently executed using the saved historical snapshot.

Both produced identical exported numerical results across all six quantitative metrics:

1. Cumulative return
2. Beta relative to SPY
3. Correlation relative to SPY
4. Annualized relative tracking error
5. Latest 20-day annualized volatility
6. Average 20-day rolling volatility

The maximum absolute difference between the two exported reports was zero at six-decimal precision.

### Run the Validation

Validate the historical snapshot:

```bash
python src/validate_data_snapshot.py
```

Validate the snapshot loader:

```bash
python src/test_snapshot_loader.py
```

Generate the consolidated risk report:

```bash
python src/generate_risk_report.py
```

Compare the standalone and dashboard CSV reports:

```bash
python src/compare_risk_reports.py
```

The comparison script expects a dashboard-exported CSV at `outputs/etf_dashboard_report.csv`.

### Limitations

The snapshot preserves adjusted closing prices but not the complete original corporate-action records or intraday market data.

Fixed historical inputs improve reproducibility, although exact results across different computing environments can also depend on Python and library versions.

SPY serves as a peer reference ETF rather than an official S&P 500 total-return benchmark.
### Index-Relative Tracking Outlier Investigation

**Historical period:** November 14, 2025 – November 13, 2026  
**Benchmark:** S&P 500 Total Return Index (`^SP500TR`), distributed through Yahoo Finance  
**Observations:** 250 aligned daily returns

#### Tracking-Error Sensitivity

The analysis identified unusually large ETF-minus-index daily return differences on June 26 and June 29, 2026.

| ETF | Full Tracking Error | Excluding June 26 & 29 | Reduction |
|---|---:|---:|---:|
| SPY | 1.0291% | 0.6088% | 40.84% |
| IVV | 1.2744% | 0.6280% | 50.73% |
| VOO | 0.8435% | 0.5494% | 34.87% |

Removing two of the 250 daily observations reduced annualized tracking error by approximately 35%–51%, demonstrating that the estimates were highly sensitive to a small number of extreme daily deviations.

The filtered estimates are sensitivity diagnostics, not replacements for the full-sample tracking-error estimates.

#### Dividend Adjustment Investigation

Raw-versus-adjusted ETF return comparisons showed that dividend adjustments did not materially affect SPY or IVV returns on June 26 or June 29.

VOO's June 26 dividend adjustment increased its measured daily return by approximately 28.89 basis points, reducing but not eliminating its index-relative tracking deviation.

#### SPY Premium/Discount Evidence

Historical premium/discount observations obtained from State Street's official SPY chart were:

| Date | Premium/Discount |
|---|---:|
| June 25, 2026 | +4.6689 bps |
| June 26, 2026 | −46.8279 bps |
| June 29, 2026 | −4.7019 bps |

SPY's premium/discount changed by −51.4968 bps on June 26 and +42.1260 bps on June 29.

These movements were directionally consistent with SPY's index-relative tracking deviations of −67.8515 bps and +47.1898 bps, respectively.

The evidence supports the hypothesis that changing ETF market-price premiums and discounts contributed to the tracking deviations.

Precise causal attribution remains unresolved because the fund-provider premium/discount methodology may use a different market-price convention from the adjusted closing prices used in the analysis.

#### IVV and VOO NAV Data Limitations

Official fund-provider historical NAV and premium/discount sources were investigated for IVV and VOO.

The required daily observations for June 25, June 26, and June 29, 2026 were not accessible through the sources examined.

Consequently, the market-price premium/discount explanation remains unverified for IVV and VOO.

#### Methodological Limitations

- ETF returns are calculated using dividend-adjusted market closing prices rather than official fund NAV total returns.
- The index benchmark uses Yahoo Finance-distributed S&P 500 Total Return Index levels.
- ETF market-price and benchmark valuation conventions may differ.
- The historical premium/discount evidence does not establish exact causal attribution.
- Full-sample tracking-error estimates remain the primary descriptive results.
- Filtered estimates are used only to assess outlier sensitivity.

**Conclusion:** A small number of synchronized late-June observations materially influenced market-price-based index-relative tracking error. SPY premium/discount evidence supports a temporary market-price dislocation hypothesis, while the precise causes of IVV and VOO deviations remain unresolved.