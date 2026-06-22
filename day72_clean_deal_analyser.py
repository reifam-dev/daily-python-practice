"""
Day 72 – Pandas Advanced: GroupBy & Aggregation
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

import pandas as pd


class DealAnalyser:
    """Analyses real estate deal data using Pandas GroupBy and aggregation."""

    def __init__(self, data: dict) -> None:
        """Initialise the analyser with a dictionary of deal data.

        Args:
            data: Dictionary with keys 'sector', 'region', 'value', 'income'.
        """
        self._df: pd.DataFrame = pd.DataFrame(data)

    def mean_by_sector(self) -> pd.Series:
        """Calculate mean deal value grouped by sector.

        Returns:
            Series indexed by sector with mean values.
        """
        return self._df.groupby("sector")["value"].mean()

    def total_by_region(self) -> pd.Series:
        """Calculate total deal value grouped by region.

        Returns:
            Series indexed by region with summed values.
        """
        return self._df.groupby("region")["value"].sum()

    def summary(self) -> pd.DataFrame:
        """Produce a multi-aggregate summary grouped by sector.

        Returns:
            DataFrame with mean, sum, and count per sector.
        """
        return self._df.groupby("sector")["value"].agg(["mean", "sum", "count"])

    def top_deals(self, n: int = 3) -> pd.DataFrame:
        """Return the top n deals by value.

        Args:
            n: Number of top deals to return; defaults to 3.

        Returns:
            DataFrame of the n largest deals by value.
        """
        return self._df.nlargest(n, "value")

    def filter_above(self, threshold: float) -> pd.DataFrame:
        """Filter deals above a given value threshold.

        Args:
            threshold: Minimum deal value to include.

        Returns:
            Filtered DataFrame.
        """
        return self._df[self._df["value"] > threshold]

    def add_yield_column(self) -> None:
        """Add a computed net initial yield (%) column to the DataFrame."""
        self._df["yield"] = self._df["income"] / self._df["value"] * 100

    def pivot_by_region(self) -> pd.DataFrame:
        """Produce a pivot table of mean deal value by sector and region.

        Returns:
            Pivot table DataFrame.
        """
        return self._df.pivot_table(
            values="value",
            index="sector",
            columns="region",
            aggfunc="mean"
        )

    def sorted_by_value(self, ascending: bool = False) -> pd.DataFrame:
        """Sort deals by value.

        Args:
            ascending: If True, sort ascending; defaults to False (descending).

        Returns:
            Sorted DataFrame.
        """
        return self._df.sort_values("value", ascending=ascending)

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for the DealAnalyser instance.
        """
        return f"DealAnalyser(rows={len(self._df)}, columns={list(self._df.columns)})"


if __name__ == "__main__":
    data: dict = {
        "sector": ["Office", "Retail", "Office", "Industrial", "Retail", "Industrial"],
        "region": ["London", "Manchester", "London", "Birmingham", "London", "Manchester"],
        "value": [50.0, 30.0, 80.0, 40.0, 25.0, 60.0],
        "income": [3.0, 2.1, 4.8, 2.8, 1.5, 4.2],
    }

    da = DealAnalyser(data)
    print("Mean by sector:\n", da.mean_by_sector())
    print("\nTotal by region:\n", da.total_by_region())
    print("\nSummary:\n", da.summary())
    print("\nTop 3 deals:\n", da.top_deals())
    da.add_yield_column()
    print("\nPivot table:\n", da.pivot_by_region())
    print("\nSorted descending:\n", da.sorted_by_value())
    print(repr(da))