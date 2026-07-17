"""Day 98 - Pandas Advanced: Portfolio Concentration Analyser.

Demonstrates method chaining with pipe(), categorical dtypes,
groupby with idxmax, and query() for filtering - PCPP1 standard.
"""
from __future__ import annotations

import pandas as pd

_DEALS = pd.DataFrame({
    "deal_name": [
        "Riverside JV", "Logistics Portfolio", "Westgate Retail",
        "Midtown Office", "Docklands Logistics",
    ],
    "region": ["London", "Midlands", "London", "London", "Midlands"],
    "sector": ["Residential", "Logistics", "Retail", "Office", "Logistics"],
    "market_value": [12_500_000.0, 34_200_000.0, 8_100_000.0, 21_000_000.0, 15_750_000.0],
})


def add_sector_category(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the sector column to a memory-efficient categorical dtype."""
    df["sector"] = df["sector"].astype("category")
    return df


def add_concentration(df: pd.DataFrame) -> pd.DataFrame:
    """Add each deal's percentage share of total portfolio value."""
    total = df["market_value"].sum()
    df["concentration_pct"] = df["market_value"] / total * 100
    return df


def top_deal_by_region(df: pd.DataFrame) -> pd.Series:
    """Return the largest deal's name for each region."""
    grouped = df.groupby("region")["market_value"]
    top_idx = grouped.idxmax()
    return df.loc[top_idx, "deal_name"]


def largest_sector_exposure(df: pd.DataFrame) -> str:
    """Return the sector with the highest total market value."""
    exposure = df.groupby("sector", observed=True)["market_value"].sum()
    return exposure.idxmax()


def high_value_deals(df: pd.DataFrame, threshold: float = 20_000_000.0) -> pd.DataFrame:
    """Return deals with a market value above the given threshold."""
    return df.query("market_value > @threshold")


if __name__ == "__main__":
    result = _DEALS.pipe(add_sector_category).pipe(add_concentration)
    print(result)
    print(top_deal_by_region(result))
    print(largest_sector_exposure(result))
    print(high_value_deals(result))