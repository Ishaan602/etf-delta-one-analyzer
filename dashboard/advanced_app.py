"""Standalone advanced Streamlit app; does not overwrite dashboard/app.py."""
import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from advanced_tracking import (load_prices, returns_from_prices, tracking_summary,
                               daily_tracking_differences, rolling_tracking_table, TICKERS, BENCHMARK)

st.set_page_config(page_title='ETF Delta One | Advanced Index Tracking', page_icon='📈', layout='wide')
st.title('ETF Delta One — Advanced Index Tracking')
st.caption('Reproducible research from saved ETF adjusted-close and S&P 500 total-return index snapshots.')

@st.cache_data

def get_data():
    p = load_prices()
    r = returns_from_prices(p)
    return p, r, tracking_summary(p, r)

try:
    prices, returns, summary = get_data()
except Exception as exc:
    st.error('Could not load saved snapshots. See SETUP.md for required file paths.')
    st.exception(exc)
    st.stop()

st.sidebar.header('Analysis controls')
page = st.sidebar.radio('View', ['Index tracking overview', 'Rolling tracking error', 'Daily deviations', 'Research report'])
window = st.sidebar.selectbox('Rolling window (trading days)', [20, 60], index=0)
selected = st.sidebar.multiselect('ETFs', list(TICKERS), default=list(TICKERS))
st.sidebar.caption(f'{prices.index[0].date()} to {prices.index[-1].date()} | {len(returns)} daily returns')

if page == 'Index tracking overview':
    st.subheader('Full-period ETF versus benchmark performance')
    cumulative = (prices.div(prices.iloc[0]) - 1) * 100
    st.line_chart(cumulative, y_label='Cumulative return (%)')
    st.subheader('Index-relative tracking metrics')
    st.dataframe(summary.round(4), use_container_width=True)
    st.info('SP500TR is a Yahoo Finance-distributed gross total-return index series; ETF returns use adjusted market closing prices, not NAV.')
elif page == 'Rolling tracking error':
    st.subheader(f'{window}-day rolling annualized tracking error')
    if not selected:
        st.warning('Select at least one ETF.')
    else:
        rolling = rolling_tracking_table(returns, window) * 100
        st.line_chart(rolling[selected], y_label='Annualized tracking error (%)')
        st.dataframe(rolling[selected].agg(['mean', 'max']).round(4), use_container_width=True)
        st.caption('Rolling windows overlap; large outliers affect each window that contains them.')
elif page == 'Daily deviations':
    st.subheader('Daily ETF minus index returns')
    deviations = daily_tracking_differences(returns) * 10000
    if selected:
        st.line_chart(deviations[selected], y_label='Tracking difference (bps)')
        st.dataframe(deviations[selected].round(4), use_container_width=True)
    else:
        st.warning('Select at least one ETF.')
    st.caption('June 26 and 29, 2026 are notable sensitivity dates; do not silently remove them from the primary analysis.')
else:
    st.subheader('Index-relative tracking report')
    st.dataframe(summary.round(6), use_container_width=True)
    st.download_button('Download index tracking report (CSV)', summary.to_csv(index_label='ETF', float_format='%.6f'), file_name='index_tracking_report.csv', mime='text/csv')
    st.markdown('''**Methodology:** Tracking error is the sample standard deviation of daily ETF-minus-index returns, annualized using √252. Filtered estimates omit June 26 and June 29 solely for sensitivity analysis. Historical premium/discount evidence supports a possible market-price effect for SPY, but exact causal attribution is unconfirmed; equivalent historical NAV data for IVV and VOO was unavailable in the sources examined. This analysis is educational, not investment advice.''')
