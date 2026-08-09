"""Day 121 - Time Series Resampling and Gap Filling: Deal Valuation Series.

Resamples an irregular daily valuation series to a continuous daily
frequency, forward-fills the resulting gaps (the last known value
carries forward, which is the standard convention for valuation
marks), and computes a rolling average over the filled series -
PCPP1 standard.
"""
from __future__ import annotations

import pandas as pd

_DATES = pd.to_datetime([
    "2026-01-01", "2026-01-02", "2026-01-05", "2026-01-06", "2026-01-10",
])
_VALUES = [100.0, 101.5, None, 104.0, 108.0]


def build_series() -> pd.Series:
    """Build the raw, irregularly-spaced valuation series."""
    return pd.Series(_VALUES, index=_DATES, name="valuation")


def fill_gaps(series: pd.Series) -> pd.Series:
    """Resample to daily frequency and forward-fill any resulting gaps."""
    daily = series.resample("D").asfreq()
    return daily.ffill()


def rolling_average(series: pd.Series, window: int) -> pd.Series:
    """Compute a rolling average over the given window size."""
    return series.rolling(window).mean()


if __name__ == "__main__":
    raw = build_series()
    print("Raw series:")
    print(raw)

    filled = fill_gaps(raw)
    print("\nFilled (daily frequency):")
    print(filled)

    avg = rolling_average(filled, window=3)
    print("\n3-day rolling average:")
    print(avg)