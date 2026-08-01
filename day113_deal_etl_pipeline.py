"""Day 113 - ETL Pipeline: Deal ETL Pipeline.

A minimal Extract-Transform-Load pipeline: pulls raw deal data,
derives risk flags, and loads it into SQLite - with the connection
properly closed and parameterised queries used throughout -
PCPP1 standard.
"""
from __future__ import annotations

import sqlite3
from contextlib import closing

import pandas as pd

_RAW_DEALS = pd.DataFrame({
    "deal_name": ["Riverside JV", "Logistics Portfolio", "Westgate Retail"],
    "region": ["London", "Midlands", "London"],
    "market_value": [12_500_000.0, 34_200_000.0, 8_100_000.0],
    "ltv": [0.60, 0.55, 0.65],
})

_LTV_RISK_THRESHOLD = 0.65


def extract() -> pd.DataFrame:
    """Simulate pulling raw deal records from a source system."""
    return _RAW_DEALS.copy()


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Derive an LTV percentage column and a boolean risk flag."""
    df = df.copy()
    df["ltv_pct"] = df["ltv"] * 100
    df["risk_flag"] = df["ltv"] > _LTV_RISK_THRESHOLD
    return df


def load(df: pd.DataFrame, db_path: str) -> None:
    """Load the transformed data into a SQLite table, closing the connection."""
    with closing(sqlite3.connect(db_path)) as connection:
        df.to_sql("deals", connection, if_exists="replace", index=False)
        connection.commit()


def query_high_ltv_deals(db_path: str, threshold: float) -> list[tuple]:
    """Return deals above a given LTV percentage, using a parameterised query."""
    with closing(sqlite3.connect(db_path)) as connection:
        cursor = connection.execute(
            "SELECT deal_name, ltv_pct FROM deals WHERE ltv_pct > ?",
            (threshold,),
        )
        return cursor.fetchall()


def run_pipeline(db_path: str = "deals.db") -> None:
    """Run the full extract-transform-load pipeline."""
    raw = extract()
    clean = transform(raw)
    load(clean, db_path)

    for row in query_high_ltv_deals(db_path, threshold=60.0):
        print(row)


if __name__ == "__main__":
    run_pipeline()