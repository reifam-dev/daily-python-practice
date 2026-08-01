"""Day 113 - ETL Pipeline: Error Quiz.

Find and fix three bugs. No location hints.
"""
import sqlite3

import pandas as pd

RAW_DEALS = pd.DataFrame({
    "deal_name": ["Riverside JV", "Logistics Portfolio", "Westgate Retail"],
    "region": ["London", "Midlands", "London"],
    "market_value": [12_500_000.0, 34_200_000.0, 8_100_000.0],
    "ltv": [0.60, 0.55, 0.65],
})


def extract() -> pd.DataFrame:
    return RAW_DEALS.copy()


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df["ltv_pct"] = df["ltv"] * 100
    df["risk_flag"] = df["ltv"] > 0.65
    return df


def load(df: pd.DataFrame, db_path: str) -> None:
    connection = sqlite3.connect(db_path)
    df.to_sql("deals", connection, if_exists="replace")


def run_pipeline(db_path: str = "deals.db") -> None:
    raw = extract()
    clean = transform(raw)
    load(clean, db_path)

    connection = sqlite3.connect(db_path)
    result = connection.execute("SELECT deal_name, ltv_pct FROM deals")
    for row in result:
        print(row)


if __name__ == "__main__":
    run_pipeline()