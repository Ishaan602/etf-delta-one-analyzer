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

**Phase 4 — Interactive Streamlit Dashboard**

The next phase will integrate the existing calculations into an interactive financial analytics application with ETF selection, performance comparisons, quantitative risk metrics, and automated reporting.
## Quantitative Risk Analysis — Preliminary Findings

Using approximately one year of dividend-adjusted historical prices for SPY, IVV, and VOO, I analyzed daily return differences, annualized relative tracking error, and short-term reversal behavior.

### Key Findings

- **Relative tracking error:** IVV exhibited 0.5364% annualized tracking error relative to SPY, compared with 0.3853% for VOO.
- **Outlier sensitivity:** Excluding five trading days between June 25 and July 1, 2026 reduced the estimated relative tracking error by 35.63% for IVV and 28.52% for VOO.
- **Dividend adjustments:** An investigation of dividend events and adjusted versus unadjusted prices showed that distributions explained several large raw-return differences but did not fully account for the late-June deviations.
- **Short-term reversals:** IVV and VOO exhibited negative lag-1 correlations of −0.4344 and −0.5165, respectively, with next-day sign reversal rates of 65.06% and 69.08%.
- **Robustness:** After excluding the late-June outlier period, lag-1 correlations remained negative at −0.4799 for IVV and −0.4844 for VOO.

### Interpretation

The results suggest that daily return differences between ETFs tracking the same index frequently reverse over short horizons. This pattern is consistent with temporary relative-price fluctuations, although additional data would be required to establish the underlying cause.

These findings are descriptive and do not demonstrate a profitable trading strategy. Further analysis of historical NAVs, market microstructure, and transaction costs would be necessary.

**Methodology note:** SPY was used as a peer reference ETF, not as an official S&P 500 total-return benchmark. Results are based on historical adjusted-price data and should be interpreted as relative ETF tracking analysis.

## Disclaimer

This project is intended for educational and portfolio purposes only and does not constitute investment advice.