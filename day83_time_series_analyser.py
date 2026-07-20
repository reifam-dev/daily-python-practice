"""
Day 83 – Pandas Advanced: time series, resampling, rolling windows, cumulative returns.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

import pandas as pd


class TimeSeriesAnalyser:
    """Analyses real estate return time series using Pandas time series tools."""

    def __init__(self, data: dict) -> None:
        """Initialise with a dictionary containing a 'date' key and return columns.

        Args:
            data: Dictionary with 'date' and one or more numeric return columns.
        """
        self._df: pd.DataFrame = pd.DataFrame(data)
        self._df["date"] = pd.to_datetime(self._df["date"])
        self._df = self._df.set_index("date")

    def monthly_mean(self) -> pd.DataFrame:
        """Resample to monthly frequency and compute mean return.

        Returns:
            Monthly mean return DataFrame.
        """
        return self._df.resample("ME").mean()

    def quarterly_total(self) -> pd.DataFrame:
        """Resample to quarterly frequency and compute total return.

        Returns:
            Quarterly total return DataFrame.
        """
        return self._df.resample("QE").sum()

    def rolling_average(self, window: int = 3) -> pd.DataFrame:
        """Compute rolling mean over a given window.

        Args:
            window: Number of periods for the rolling window; defaults to 3.

        Returns:
            Rolling mean DataFrame.
        """
        return self._df.rolling(window).mean()

    def pct_change(self) -> pd.DataFrame:
        """Compute period-over-period percentage change.

        Returns:
            Percentage change DataFrame.
        """
        return self._df.pct_change() * 100

    def cumulative_return(self) -> pd.DataFrame:
        """Compute cumulative compounded return series.

        Returns:
            Cumulative return DataFrame.
        """
        return (1 + self._df).cumprod() - 1

    def fill_missing(self) -> pd.DataFrame:
        """Forward-fill then backward-fill missing values.

        Returns:
            DataFrame with missing values filled.
        """
        return self._df.ffill().bfill()

    def annualised_return(self) -> pd.Series:
        """Compute annualised return assuming monthly data.

        Returns:
            Annualised return per column as a Series.
        """
        total = (1 + self._df).prod()
        n = len(self._df)
        return total ** (12 / n) - 1

    def drawdown(self) -> pd.DataFrame:
        """Compute drawdown series for each column.

        Returns:
            Drawdown DataFrame showing decline from running peak.
        """
        cumulative = (1 + self._df).cumprod()
        running_max = cumulative.cummax()
        return (cumulative - running_max) / running_max

    def summary_stats(self) -> pd.DataFrame:
        """Produce a summary statistics table across all columns.

        Returns:
            DataFrame with mean, std, min, max, and annualised return.
        """
        stats = pd.DataFrame({
            "mean": self._df.mean(),
            "volatility": self._df.std(),
            "min": self._df.min(),
            "max": self._df.max(),
            "annualised": self.annualised_return(),
        })
        return stats

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this analyser.
        """
        return (
            f"TimeSeriesAnalyser(rows={len(self._df)}, "
            f"columns={list(self._df.columns)})"
        )


if __name__ == "__main__":
    data: dict = {
        "date": pd.date_range("2025-01-01", periods=12, freq="ME"),
        "office": [0.04, 0.03, 0.05, 0.02, 0.06, 0.03, 0.04, 0.05, 0.02, 0.03, 0.06, 0.04],
        "retail": [0.03, 0.02, 0.04, 0.01, 0.05, 0.02, 0.03, 0.04, 0.01, 0.02, 0.05, 0.03],
    }

    ts = TimeSeriesAnalyser(data)
    print(repr(ts))
    print("\nMonthly mean:\n", ts.monthly_mean())
    print("\nQuarterly total:\n", ts.quarterly_total())
    print("\nRolling 3-month average:\n", ts.rolling_average())
    print("\nCumulative return:\n", ts.cumulative_return())
    print("\nAnnualised return:\n", ts.annualised_return())
    print("\nDrawdown:\n", ts.drawdown())
    print("\nSummary stats:\n", ts.summary_stats())