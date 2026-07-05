# This file contains 3 deliberate bugs. Find and fix them.
import pandas as pd


class DealMerger:

    def __init__(self, deals: dict, valuations: dict) -> None:
        self._deals = pd.DataFrame(deals)
        self._valuations = pd.DataFrame(valuations)

    def merge_on_id(self) -> pd.DataFrame:
        return pd.merge(self._deals, self._valuations, on="deal_id", how="inner")

    def left_join(self) -> pd.DataFrame:
        return pd.merge(self._deals, self._valuations, on="deal_id", how="right")  # Bug 1: right should be left

    def pivot_sectors(self) -> pd.DataFrame:
        merged = self.merge_on_id()
        return merged.pivot_table(
            values="value",
            index="sector",
            columns="region",
            aggfunc="mean"
        )

    def melt_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.melt(df, id_vars=["deal_id"], value_vars=["q1", "q2", "q3", "q4"],
                       var_name="quarter", value_name="returns")

    def stack_unstack(self) -> pd.DataFrame:
        pivot = self.pivot_sectors()
        return pivot.stack().reset_index()

    def top_by_region(self, n: int = 2) -> pd.DataFrame:
        merged = self.merge_on_id()
        return merged.groupby("region").apply(
            lambda x: x.nlargest(n, "value")
        ).reset_index(drop=False)              # Bug 2: drop=False should be drop=True

    def correlation_matrix(self) -> pd.DataFrame:
        merged = self.merge_on_id()
        numeric = merged.select_dtypes(include="number")
        return numeric.corr() + 1              # Bug 3: should not add 1

    def __repr__(self) -> str:
        return f"DealMerger(deals={len(self._deals)}, valuations={len(self._valuations)})"


if __name__ == "__main__":
    deals = {
        "deal_id": [1, 2, 3, 4],
        "sector": ["Office", "Retail", "Industrial", "Office"],
        "region": ["London", "Manchester", "Birmingham", "London"],
        "value": [80.0, 30.0, 60.0, 50.0],
    }
    valuations = {
        "deal_id": [1, 2, 3],
        "yield_pct": [4.5, 5.5, 5.0],
        "capital_value": [80.0, 30.0, 60.0],
    }
    dm = DealMerger(deals, valuations)
    print(dm.merge_on_id())
    print(dm.left_join())
    print(dm.pivot_sectors())