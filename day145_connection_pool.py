"""Day 145 - Database Connection Pooling: Deal Connection Pool.

Reuses a fixed set of connections rather than opening a new one per
request. acquire() only hands out a connection that isn't already in
use, and raises clearly once the pool is exhausted rather than
silently handing out a connection someone else is mid-query on -
PCPP1 standard.
"""
from __future__ import annotations


class FakeConnection:
    """Stand-in for a real database connection."""

    def __init__(self, conn_id: int) -> None:
        self.conn_id = conn_id
        self.in_use = False

    def execute(self, query: str) -> str:
        return f"conn-{self.conn_id} executed: {query}"


class PoolExhaustedError(Exception):
    """Raised when no connection is available in the pool."""


class ConnectionPool:
    """A fixed-size pool of reusable connections."""

    def __init__(self, pool_size: int) -> None:
        if pool_size <= 0:
            raise ValueError("pool_size must be positive")
        self.pool_size = pool_size
        self.connections = [FakeConnection(i) for i in range(pool_size)]

    def acquire(self) -> FakeConnection:
        """Return the first connection that isn't currently in use."""
        for conn in self.connections:
            if not conn.in_use:
                conn.in_use = True
                return conn
        raise PoolExhaustedError("No available connections")

    def release(self, conn: FakeConnection) -> None:
        """Mark a connection as free again, available for reuse."""
        conn.in_use = False


if __name__ == "__main__":
    pool = ConnectionPool(pool_size=2)

    conn_a = pool.acquire()
    print(conn_a.execute("SELECT * FROM deals"))

    conn_b = pool.acquire()
    print(conn_b.execute("SELECT * FROM investors"))

    try:
        pool.acquire()
    except PoolExhaustedError as exc:
        print(f"Rejected: {exc}")

    pool.release(conn_a)
    print("Released conn_a")

    conn_c = pool.acquire()
    print(conn_c.execute("SELECT * FROM deals WHERE region = 'London'"))