"""Reproducible ETF/index analytics using immutable local price snapshots."""
from pathlib import Path
import numpy as np
import pandas as pd

ETF_FILE = 'etf_adjusted_prices_2025-11-14_2026-11-13.csv'
INDEX_FILE = 'sp500_total_return_2025-11-14_2026-11-13.csv'
TICKERS = ('SPY', 'IVV', 'VOO')
BENCHMARK = 'SP500TR'
ANNUALIZATION = 252
OUTLIERS = pd.to_datetime(['2026-06-26', '2026-06-29'])


def load_prices(data_dir=None):
    directory = Path(data_dir) if data_dir else Path(__file__).resolve().parents[1] / 'data'
    a = pd.read_csv(directory / ETF_FILE, index_col='Date', parse_dates=['Date'])
    b = pd.read_csv(directory / INDEX_FILE, index_col='Date', parse_dates=['Date'])
    if list(a.columns) != list(TICKERS) or list(b.columns) != [BENCHMARK]:
        raise ValueError('Unexpected ETF/index columns')
    if not a.index.equals(b.index) or not a.index.is_unique or not a.index.is_monotonic_increasing:
        raise ValueError('ETF and benchmark dates must match and be unique/sorted')
    p = pd.concat([a, b], axis=1).astype(float)
    if p.empty or not np.isfinite(p.to_numpy()).all() or not (p > 0).all().all():
        raise ValueError('Prices must be finite and positive')
    return p


def returns_from_prices(prices):
    returns = prices.pct_change(fill_method=None).iloc[1:]
    if returns.empty or not np.isfinite(returns.to_numpy(dtype=float)).all():
        raise ValueError('Daily returns are missing or invalid')
    return returns


def daily_tracking_differences(returns):
    return returns.loc[:, list(TICKERS)].sub(returns[BENCHMARK], axis=0)


def rolling_tracking_error(etf_returns, benchmark_returns, window=20, trading_days=252):
    if isinstance(window, bool) or not isinstance(window, int) or window < 2:
        raise ValueError('window must be an integer >= 2')
    if trading_days <= 0:
        raise ValueError('trading_days must be positive')
    aligned = pd.concat([etf_returns.rename('etf'), benchmark_returns.rename('benchmark')], axis=1, join='inner').dropna()
    if len(aligned) < window:
        raise ValueError('Not enough aligned observations')
    return (aligned['etf'] - aligned['benchmark']).rolling(window, min_periods=window).std(ddof=1) * np.sqrt(trading_days)


def rolling_tracking_table(returns, window=20):
    return pd.DataFrame({t: rolling_tracking_error(returns[t], returns[BENCHMARK], window) for t in TICKERS})


def tracking_summary(prices, returns):
    d = daily_tracking_differences(returns)
    cumulative = prices.iloc[-1] / prices.iloc[0] - 1
    rows = []
    for ticker in TICKERS:
        x = d[ticker]
        filtered = x.drop(index=OUTLIERS, errors='ignore')
        full_te = x.std(ddof=1) * np.sqrt(ANNUALIZATION) * 100
        filtered_te = filtered.std(ddof=1) * np.sqrt(ANNUALIZATION) * 100 if len(filtered) >= 2 else np.nan
        rows.append({
            'ETF': ticker,
            'Cumulative Difference (bps)': (cumulative[ticker] - cumulative[BENCHMARK]) * 10000,
            'Annualized Tracking Error (%)': full_te,
            'Mean Daily Difference (bps)': x.mean() * 10000,
            'Max Absolute Daily Deviation (bps)': x.abs().max() * 10000,
            'Filtered TE (%)': filtered_te,
            'TE Reduction (%)': (full_te - filtered_te) / full_te * 100 if full_te > 0 else np.nan,
        })
    return pd.DataFrame(rows).set_index('ETF')


def analyze(data_dir=None):
    prices = load_prices(data_dir)
    returns = returns_from_prices(prices)
    return prices, returns, tracking_summary(prices, returns)
