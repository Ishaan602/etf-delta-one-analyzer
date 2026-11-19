import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from advanced_tracking import rolling_tracking_error, load_prices, returns_from_prices, tracking_summary, rolling_tracking_table


def test_rolling_math():
    dates = pd.bdate_range('2026-01-05', periods=6)
    etf = pd.Series([.010, -.005, .008, .012, -.003, .006], index=dates)
    benchmark = pd.Series([.009, -.004, .007, .010, -.002, .005], index=dates)
    actual = rolling_tracking_error(etf, benchmark, window=3)
    expected = np.std([.001, -.001, .001], ddof=1) * np.sqrt(252)
    assert actual.iloc[:2].isna().all()
    assert np.isclose(actual.iloc[2], expected)
    assert actual.notna().sum() == 4


def test_alignment():
    dates = pd.bdate_range('2026-01-05', periods=4)
    etf = pd.Series([.01, .02, .03, .04], index=dates)
    benchmark = pd.Series([.01, .02, .03], index=dates[:3])
    actual = rolling_tracking_error(etf, benchmark, window=2)
    assert len(actual) == 3


def test_snapshot_integration():
    root = Path(__file__).resolve().parents[1]
    if not (root / 'data' / 'etf_adjusted_prices_2025-11-14_2026-11-13.csv').exists():
        import pytest
        pytest.skip('Copy validated snapshots into data/ first')
    p = load_prices()
    r = returns_from_prices(p)
    report = tracking_summary(p, r)
    assert len(p) == 251 and len(r) == 250
    assert np.isclose((p['SP500TR'].iloc[-1] / p['SP500TR'].iloc[0] - 1) * 100, 13.5813, atol=0.0001)
    assert np.allclose(report.loc[['SPY','IVV','VOO'], 'Annualized Tracking Error (%)'], [1.0291,1.2744,.8435], atol=.001)
    for w in (20,60):
        rolling = rolling_tracking_table(r, w)
        assert rolling.notna().sum().eq(len(r)-w+1).all()
