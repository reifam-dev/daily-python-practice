"""
Day 77 – PostgreSQL with psycopg2: connection, CRUD, transactions, context managers.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: pip install psycopg2-binary
"""

import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.extensions import connection as PgConnection


class PropertyDatabase:
    """Manages PostgreSQL CRUD operations for a property portfolio table."""

    def __init__(self, dsn: str) -> None:
        """Initialise the database connection.

        Args:
            dsn: PostgreSQL data source name string
                 e.g. 'postgresql://user:pass@localhost:5432/dbname'.
        """
        self._dsn: str = dsn
        self._conn: PgConnection = psycopg2.connect(dsn)

    def create_table(self) -> None:
        """Create the properties table if it does not already exist."""
        with self._conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS properties (
                    id         SERIAL PRIMARY KEY,
                    sector     VARCHAR(50)   NOT NULL,
                    region     VARCHAR(50)   NOT NULL,
                    value      NUMERIC(12,2) NOT NULL,
                    yield_pct  NUMERIC(5,2)  NOT NULL,
                    created_at TIMESTAMPTZ   DEFAULT NOW()
                )
            """)
        self._conn.commit()

    def insert_property(
        self,
        sector: str,
        region: str,
        value: float,
        yield_pct: float,
    ) -> None:
        """Insert a new property record.

        Args:
            sector:    Property sector (e.g. 'Office').
            region:    Geographic region (e.g. 'London').
            value:     Deal value in £m.
            yield_pct: Net initial yield as a percentage.
        """
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO properties (sector, region, value, yield_pct)
                VALUES (%s, %s, %s, %s)
                """,
                (sector, region, value, yield_pct),
            )
        self._conn.commit()

    def fetch_all(self) -> list[RealDictRow]:
        """Retrieve all property records.

        Returns:
            List of RealDictRow objects (behave like dicts).
        """
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM properties ORDER BY id")
            return cur.fetchall()

    def fetch_by_sector(self, sector: str) -> list[RealDictRow]:
        """Retrieve all properties in a given sector.

        Args:
            sector: Sector string to filter by.

        Returns:
            Filtered list of property rows.
        """
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM properties WHERE sector = %s ORDER BY value DESC",
                (sector,),
            )
            return cur.fetchall()

    def update_value(self, property_id: int, new_value: float) -> None:
        """Update the deal value of a property by ID.

        Args:
            property_id: Primary key of the record to update.
            new_value:   New value in £m.
        """
        with self._conn.cursor() as cur:
            cur.execute(
                "UPDATE properties SET value = %s WHERE id = %s",
                (new_value, property_id),
            )
        self._conn.commit()

    def delete_property(self, property_id: int) -> None:
        """Delete a property record by ID.

        Args:
            property_id: Primary key of the record to delete.
        """
        with self._conn.cursor() as cur:
            cur.execute(
                "DELETE FROM properties WHERE id = %s",
                (property_id,),
            )
        self._conn.commit()

    def mean_yield_by_sector(self) -> list[RealDictRow]:
        """Compute mean yield grouped by sector using a SQL aggregate.

        Returns:
            List of rows with sector and mean_yield columns.
        """
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT sector, ROUND(AVG(yield_pct), 2) AS mean_yield
                FROM properties
                GROUP BY sector
                ORDER BY mean_yield DESC
            """)
            return cur.fetchall()

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this PropertyDatabase.
        """
        return f"PropertyDatabase(dsn='{self._dsn[:20]}...')"


if __name__ == "__main__":
    DSN = "postgresql://postgres:password@localhost:5432/property_db"
    db = PropertyDatabase(DSN)
    db.create_table()
    db.insert_property("Office", "London", 80.0, 4.5)
    db.insert_property("Retail", "Manchester", 30.0, 5.5)
    db.insert_property("Industrial", "Birmingham", 60.0, 4.8)
    print("All records:", db.fetch_all())
    db.update_value(1, 85.0)
    print("By sector:", db.fetch_by_sector("Office"))
    print("Mean yields:", db.mean_yield_by_sector())
    db.delete_property(2)
    print("After delete:", db.fetch_all())
    db.close()
    print(repr(db))