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

## Disclaimer

This project is intended for educational and portfolio purposes only and does not constitute investment advice.