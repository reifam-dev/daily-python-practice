"""Day 148 - SQL Injection Prevention: Error Quiz. Find and fix three bugs."""
import sqlite3


def setup(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS deals (name TEXT, market_value REAL)")
    conn.execute("INSERT INTO deals VALUES ('Riverside JV', 12500000.0)")
    conn.commit()
    conn.close()


def find_deal(db_path: str, name: str) -> list:
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM deals WHERE name = '" + name + "'"
    cursor = conn.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    setup("deals148.db")
    print(find_deal("deals148.db", "Riverside JV"))
    malicious = "x' OR '1'='1"
    print(find_deal("deals148.db", malicious))