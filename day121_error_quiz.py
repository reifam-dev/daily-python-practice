"""Day 121 - Time Series Resampling and Gap Filling: Error Quiz.

Find and fix three bugs. No location hints.
"""
import pandas as pd

DATES = pd.to_datetime([
    "2026-01-01", "2026-01-02", "2026-01-05", "2026-01-06", "2026-01-10",
])
VALUES = [100.0, 101.5, None, 104.0, 108.0]


def build_series() -> pd.Series:
    return pd.Series(VALUES, index=DATES)


def fill_gaps(series: pd.Series) -> pd.Series:
    daily = series.resample("D")
    filled = daily.fillna(method="ffill")
    return filled


def rolling_average(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window).mean


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