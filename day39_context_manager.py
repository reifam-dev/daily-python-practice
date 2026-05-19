# Day 39 - Clean context manager classes
# New concepts: __enter__, __exit__, contextlib.contextmanager
# PEP 8, docstrings, type hints, exceptions throughout

import time
import contextlib
from typing import Optional, Generator


class Timer:
    """A context manager that measures elapsed time for a block of code.

    Usage:
        with Timer() as t:
            # code to time
        print(t.elapsed)
    """

    def __init__(self) -> None:
        self._start: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self) -> "Timer":
        """Start the timer and return self."""
        self._start = time.time()
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        traceback: Optional[object]
    ) -> bool:
        """Stop the timer. Return False to propagate any exceptions."""
        self.elapsed = time.time() - self._start
        print(f"  Elapsed: {self.elapsed:.4f}s")
        return False


class DatabaseConnection:
    """A context manager that simulates a database connection.

    Ensures the connection is always closed after the block,
    even if an exception is raised.
    """

    def __init__(self, db_name: str) -> None:
        if not db_name or not db_name.strip():
            raise ValueError("Database name cannot be empty.")
        self._db_name: str = db_name.strip()
        self._connected: bool = False

    def __enter__(self) -> "DatabaseConnection":
        """Open the connection and return self."""
        self._connected = True
        print(f"  Connected to '{self._db_name}'")
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        traceback: Optional[object]
    ) -> bool:
        """Close the connection. Return False to propagate exceptions."""
        self._connected = False
        print(f"  Disconnected from '{self._db_name}'")
        return False

    def query(self, sql: str) -> str:
        """Run a simulated query. Raises RuntimeError if not connected."""
        if not self._connected:
            raise RuntimeError("Not connected to database.")
        return f"Result of: {sql}"

    @property
    def connected(self) -> bool:
        """Return the connection status."""
        return self._connected


@contextlib.contextmanager
def managed_resource(name: str) -> Generator[str, None, None]:
    """A generator-based context manager using @contextlib.contextmanager.

    Everything before yield is __enter__. Everything after is __exit__.
    """
    print(f"  Acquiring resource: {name}")
    try:
        yield name.upper()
    finally:
        print(f"  Releasing resource: {name}")


if __name__ == "__main__":
    print("=== Timer context manager ===\n")
    with Timer() as t:
        total = sum(range(1_000_000))
    print(f"  Sum: {total}, Time: {t.elapsed:.4f}s\n")

    print("=== DatabaseConnection context manager ===\n")
    try:
        with DatabaseConnection("ProductionDB") as db:
            print(f"  Connected: {db.connected}")
            result = db.query("SELECT * FROM users")
            print(f"  {result}")
        print(f"  Connected after block: {db.connected}\n")
    except (ValueError, RuntimeError) as e:
        print(f"  Error: {e}\n")

    print("=== contextlib.contextmanager ===\n")
    with managed_resource("database") as res:
        print(f"  Using resource: {res}")