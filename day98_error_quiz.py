"""Day 98 - Pandas Advanced: Error Quiz.

Find and fix three bugs. No location hints.
"""
import pandas as pd

DEALS = pd.DataFrame({
    "deal_name": [
        "Riverside JV", "Logistics Portfolio", "Westgate Retail",
        "Midtown Office", "Docklands Logistics",
    ],
    "region": ["London", "Midlands", "London", "London", "Midlands"],
    "sector": ["Residential", "Logistics", "Retail", "Office", "Logistics"],
    "market_value": [12_500_000.0, 34_200_000.0, 8_100_000.0, 21_000_000.0, 15_750_000.0],
})


def add_sector_category(df: pd.DataFrame) -> pd.DataFrame:
    df["sector"] = df["sector"].astype(str)
    return df


def add_concentration(df: pd.DataFrame) -> pd.DataFrame:
    total = df["market_value"].sum()
    df["concentration_pct"] = df["market_value"] / total * 100
    return df


def top_deal_by_region(df: pd.DataFrame) -> pd.Series:
    grouped = df.groupby("region")["market_value"]
    top_idx = grouped.idxmax()
    return df.loc[top_idx, "deal_name"]


def largest_sector_exposure(df: pd.DataFrame) -> str:
    exposure = df.groupby("sector")["market_value"].sum()
    return exposure.idxmax


def high_value_deals(df: pd.DataFrame) -> pd.DataFrame:
    return df.query("market_value = 20000000")


if __name__ == "__main__":
    result = DEALS.pipe(add_sector_category).pipe(add_concentration)
    print(result)
    print(top_deal_by_region(result))
    print(largest_sector_exposure(result))
    print(high_value_deals(result))