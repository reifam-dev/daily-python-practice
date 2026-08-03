"""Day 115 - Idempotent Upserts: Error Quiz.

Find and fix three bugs. No location hints.
"""
import sqlite3
from contextlib import closing

NEW_DEALS = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0},
    {"deal_name": "Logistics Portfolio", "market_value": 34_200_000.0},
]

UPDATED_DEALS = [
    {"deal_name": "Riverside JV", "market_value": 13_100_000.0},
]


def setup_table(db_path: str) -> None:
    with closing(sqlite3.connect(db_path)) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS deals ("
            "deal_name TEXT PRIMARY KEY, market_value REAL)"
        )
        connection.commit()


def upsert_deals(db_path: str, deals: list[dict]) -> None:
    with closing(sqlite3.connect(db_path)) as connection:
        for deal in deals:
            connection.execute(
                "INSERT INTO deals (deal_name, market_value) VALUES (?, ?)",
                (deal["deal_name"], deal["market_value"]),
            )
        connection.commit()


def get_all_deals(db_path: str) -> list[tuple]:
    with closing(sqlite3.connect(db_path)) as connection:
        cursor = connection.execute("SELECT deal_name, market_value FROM deals")
        return cursor.fetchall()


if __name__ == "__main__":
    db = "deals_incremental.db"
    setup_table(db)
    upsert_deals(db, NEW_DEALS)
    upsert_deals(db, UPDATED_DEALS)
    for row in get_all_deals(db):
        print(row)