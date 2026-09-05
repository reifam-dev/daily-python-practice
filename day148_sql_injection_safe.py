"""Day 148 - SQL Injection Prevention: parameterised queries only,
never string-concatenated SQL - PCPP1 standard."""
from __future__ import annotations
import sqlite3
from contextlib import closing


def setup(db_path: str) -> None:
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS deals (name TEXT, market_value REAL)")
        conn.execute("INSERT INTO deals VALUES ('Riverside JV', 12500000.0)")
        conn.commit()


def find_deal(db_path: str, name: str) -> list:
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.execute("SELECT * FROM deals WHERE name = ?", (name,))
        return cursor.fetchall()


if __name__ == "__main__":
    setup("deals148.db")
    print(find_deal("deals148.db", "Riverside JV"))
    malicious = "x' OR '1'='1"
    print(find_deal("deals148.db", malicious))  # returns [], not every row