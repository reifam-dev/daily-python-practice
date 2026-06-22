# This file contains 3 deliberate bugs. Find and fix them.
import pandas as pd


class DealAnalyser:

    def __init__(self, data: dict) -> None:
        self._df = pd.DataFrame(data)

    def mean_by_sector(self) -> pd.Series:
        return self._df.groupby("sector")["value"].mean()

    def total_by_region(self) -> pd.Series:
        return self._df.groupby("region")["value"].sum()

    def deal_count(self) -> pd.Series:
        return self._df.groupby("sector").count()

    def top_deals(self, n: int = 3) -> pd.DataFrame:
        return self._df.nlargest(n, "value")

    def summary(self) -> pd.DataFrame:
        return self._df.groupby("sector")["value"].agg(["mean", "sum", "count"])

    def filter_above(self, threshold: float) -> pd.DataFrame:
        return self._df[self._df["value"] > threshold]

    def add_yield_column(self) -> None:
        self._df["yield"] = self._df["income"] / self._df["value"] * 100  # Bug 1: integer division


if __name__ == "__main__":
    data = {
        "sector": ["Office", "Retail", "Office", "Industrial", "Retail", "Industrial"],
        "region": ["London", "Manchester", "London", "Birmingham", "London", "Manchester"],
        "value": [50.0, 30.0, 80.0, 40.0, 25.0, 60.0],
        "income": [3.0, 2.1, 4.8, 2.8, 1.5, 4.2]
    }
    da = DealAnalyser(data)
    print(da.mean_by_sector())
    print(da.summary())
    da.add_yield_column()
    grouped = da._df.groupby("sector")["yield"].mean()
    print(grouped)
    pivoted = da._df.pivot_table(values="value", index="sector", columns="region", aggfunc="sum")  # Bug 2: wrong aggfunc
    print(pivoted)
    sorted_df = da._df.sort_values("value", ascending=True)   # Bug 3: should be descending
    print(sorted_df)