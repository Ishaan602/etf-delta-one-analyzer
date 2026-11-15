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

## Current Status

Phase 1 — Development environment and initial project structure completed.

Market data analysis and risk calculations are under development.
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