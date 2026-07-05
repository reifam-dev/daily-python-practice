# This file contains 3 deliberate bugs. Find and fix them.
import pandas as pd
import numpy as np


class TimeSeriesAnalyser:

    def __init__(self, data: dict) -> None:
        self._df = pd.DataFrame(data)
        self._df["date"] = pd.to_datetime(self._df["date"])
        self._df = self._df.set_index("date")

    def monthly_mean(self) -> pd.DataFrame:
        return self._df.resample("M").mean()

    def quarterly_total(self) -> pd.DataFrame:
        return self._df.resample("Q").sum()

    def rolling_average(self, window: int = 3) -> pd.DataFrame:
        return self._df.rolling(window).mean()

    def pct_change(self) -> pd.DataFrame:
        return self._df.pct_change() * 100

    def cumulative_return(self) -> pd.DataFrame:
        return (1 + self._df / 100).cumprod() - 1  # Bug 1: dividing by 100 incorrectly — values already decimals

    def fill_missing(self) -> pd.DataFrame:
        return self._df.fillna(method="bfill")      # Bug 2: should be ffill first then bfill

    def annualised_return(self) -> pd.Series:
        total = (1 + self._df).prod()
        n = len(self._df) + 12                      # Bug 3: should not add 12
        return total ** (12 / n) - 1

    def __repr__(self) -> str:
        return f"TimeSeriesAnalyser(rows={len(self._df)}, columns={list(self._df.columns)})"


if __name__ == "__main__":
    data = {
        "date": pd.date_range("2025-01-01", periods=12, freq="ME"),
        "office": [0.04, 0.03, 0.05, 0.02, 0.06, 0.03, 0.04, 0.05, 0.02, 0.03, 0.06, 0.04],
        "retail": [0.03, 0.02, 0.04, 0.01, 0.05, 0.02, 0.03, 0.04, 0.01, 0.02, 0.05, 0.03],
    }
    ts = TimeSeriesAnalyser(data)
    print(repr(ts))
    print(ts.monthly_mean())
    print(ts.rolling_average())
    print(ts.annualised_return())