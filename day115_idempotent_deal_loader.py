"""Day 115 - Idempotent Upserts: Idempotent Deal Loader.

Loads deal records using SQLite's INSERT ... ON CONFLICT syntax, so
re-running the same load (or loading an updated record for a deal
that already exists) updates the row in place rather than creating a
duplicate or raising a constraint error - PCPP1 standard.
"""
from __future__ import annotations

import sqlite3
from contextlib import closing

_NEW_DEALS: list[dict] = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0},
    {"deal_name": "Logistics Portfolio", "market_value": 34_200_000.0},
]

_UPDATED_DEALS: list[dict] = [
    {"deal_name": "Riverside JV", "market_value": 13_100_000.0},
]


def setup_table(db_path: str) -> None:
    """Create the deals table if it doesn't already exist."""
    with closing(sqlite3.connect(db_path)) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS deals ("
            "deal_name TEXT PRIMARY KEY, market_value REAL)"
        )
        connection.commit()


def upsert_deals(db_path: str, deals: list[dict]) -> None:
    """Insert new deals or update existing ones by deal_name, idempotently."""
    with closing(sqlite3.connect(db_path)) as connection:
        for deal in deals:
            connection.execute(
                "INSERT INTO deals (deal_name, market_value) VALUES (?, ?) "
                "ON CONFLICT(deal_name) DO UPDATE SET market_value = excluded.market_value",
                (deal["deal_name"], deal["market_value"]),
            )
        connection.commit()


def get_all_deals(db_path: str) -> list[tuple]:
    """Return all deals currently stored."""
    with closing(sqlite3.connect(db_path)) as connection:
        cursor = connection.execute(
            "SELECT deal_name, market_value FROM deals ORDER BY deal_name"
        )
        return cursor.fetchall()


if __name__ == "__main__":
    db = "deals_incremental.db"
    setup_table(db)
    upsert_deals(db, _NEW_DEALS)
    upsert_deals(db, _NEW_DEALS)  # re-running the same load must not duplicate
    upsert_deals(db, _UPDATED_DEALS)  # must update in place, not add a row
    for row in get_all_deals(db):
        print(row)