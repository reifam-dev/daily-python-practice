"""
Day 85 – Pandas Advanced: merge, join, pivot, melt, stack/unstack, reshape.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

import pandas as pd


class DealMerger:
    """Merges, joins and reshapes real estate deal DataFrames."""

    def __init__(self, deals: dict, valuations: dict) -> None:
        """Initialise with deal and valuation data dictionaries.

        Args:
            deals:      Dictionary with deal data including 'deal_id'.
            valuations: Dictionary with valuation data including 'deal_id'.
        """
        self._deals: pd.DataFrame = pd.DataFrame(deals)
        self._valuations: pd.DataFrame = pd.DataFrame(valuations)

    def merge_on_id(self) -> pd.DataFrame:
        """Inner join deals and valuations on deal_id.

        Returns:
            Merged DataFrame containing only matching deal_ids.
        """
        return pd.merge(self._deals, self._valuations, on="deal_id", how="inner")

    def left_join(self) -> pd.DataFrame:
        """Left join deals and valuations, preserving all deals.

        Returns:
            Merged DataFrame with all deals; NaN for unmatched valuations.
        """
        return pd.merge(self._deals, self._valuations, on="deal_id", how="left")

    def outer_join(self) -> pd.DataFrame:
        """Outer join deals and valuations, preserving all rows.

        Returns:
            Merged DataFrame with all rows from both DataFrames.
        """
        return pd.merge(self._deals, self._valuations, on="deal_id", how="outer")

    def pivot_sectors(self) -> pd.DataFrame:
        """Pivot mean deal value by sector and region.

        Returns:
            Pivot table DataFrame.
        """
        merged = self.merge_on_id()
        return merged.pivot_table(
            values="value",
            index="sector",
            columns="region",
            aggfunc="mean",
        )

    def melt_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Melt quarterly return columns into long format.

        Args:
            df: Wide-format DataFrame with 'deal_id' and quarter columns.

        Returns:
            Long-format DataFrame with 'quarter' and 'returns' columns.
        """
        return pd.melt(
            df,
            id_vars=["deal_id"],
            value_vars=["q1", "q2", "q3", "q4"],
            var_name="quarter",
            value_name="returns",
        )

    def stack_unstack(self) -> pd.DataFrame:
        """Stack the pivot table into a long Series then reset index.

        Returns:
            Long-format DataFrame from stacked pivot.
        """
        pivot = self.pivot_sectors()
        return pivot.stack().reset_index()

    def top_by_region(self, n: int = 2) -> pd.DataFrame:
        """Return the top n deals by value within each region.

        Args:
            n: Number of top deals per region; defaults to 2.

        Returns:
            Filtered DataFrame of top deals per region.
        """
        merged = self.merge_on_id()
        return merged.groupby("region").apply(
            lambda x: x.nlargest(n, "value")
        ).reset_index(drop=True)

    def correlation_matrix(self) -> pd.DataFrame:
        """Compute correlation matrix across numeric columns.

        Returns:
            Correlation matrix DataFrame.
        """
        merged = self.merge_on_id()
        numeric = merged.select_dtypes(include="number")
        return numeric.corr()

    def summary_by_sector(self) -> pd.DataFrame:
        """Aggregate deal statistics grouped by sector.

        Returns:
            DataFrame with mean, sum, and count per sector.
        """
        merged = self.merge_on_id()
        return merged.groupby("sector").agg(
            mean_value=("value", "mean"),
            total_value=("value", "sum"),
            deal_count=("deal_id", "count"),
            mean_yield=("yield_pct", "mean"),
        )

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this merger.
        """
        return (
            f"DealMerger(deals={len(self._deals)}, "
            f"valuations={len(self._valuations)})"
        )


if __name__ == "__main__":
    deals: dict = {
        "deal_id": [1, 2, 3, 4],
        "sector": ["Office", "Retail", "Industrial", "Office"],
        "region": ["London", "Manchester", "Birmingham", "London"],
        "value": [80.0, 30.0, 60.0, 50.0],
    }
    valuations: dict = {
        "deal_id": [1, 2, 3],
        "yield_pct": [4.5, 5.5, 5.0],
        "capital_value": [80.0, 30.0, 60.0],
    }

    dm = DealMerger(deals, valuations)
    print(repr(dm))
    print("\nInner join:\n", dm.merge_on_id())
    print("\nLeft join:\n", dm.left_join())
    print("\nOuter join:\n", dm.outer_join())
    print("\nPivot sectors:\n", dm.pivot_sectors())
    print("\nTop by region:\n", dm.top_by_region())
    print("\nCorrelation:\n", dm.correlation_matrix())
    print("\nSummary by sector:\n", dm.summary_by_sector())