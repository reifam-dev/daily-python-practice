# This file contains 3 deliberate bugs. Find and fix them.
import psycopg2
from psycopg2.extras import RealDictCursor


class PropertyDatabase:

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._conn = psycopg2.connect(dsn)

    def create_table(self) -> None:
        with self._conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS properties (
                    id SERIAL PRIMARY KEY,
                    sector VARCHAR(50),
                    value NUMERIC(12, 2),
                    yield_pct NUMERIC(5, 2)
                )
            """)
        self._conn.commit()

    def insert_property(self, sector: str, value: float, yield_pct: float) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                "INSERT INTO properties (sector, value, yield_pct) VALUES (%s, %s, %s)",
                (sector, value, yield_pct)
            )
        self._conn.commit                       # Bug 1: missing parentheses

    def fetch_all(self) -> list[dict]:
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM properties")
            return cur.fetchall()

    def update_value(self, property_id: int, new_value: float) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                "UPDATE properties SET value = %s WHERE id = %s",
                (property_id, new_value)        # Bug 2: args reversed
            )
        self._conn.commit()

    def delete_property(self, property_id: int) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                "DELETE FROM properties WHERE id = %s",
                property_id                     # Bug 3: should be (property_id,)
            )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()