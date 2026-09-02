"""Day 145 - Database Connection Pooling: Error Quiz.

Find and fix three bugs. No location hints.
"""
class FakeConnection:
    def __init__(self, conn_id: int):
        self.conn_id = conn_id
        self.in_use = False

    def execute(self, query: str) -> str:
        return f"conn-{self.conn_id} executed: {query}"


class ConnectionPool:
    def __init__(self, pool_size: int):
        self.pool_size = pool_size
        self.connections = [FakeConnection(i) for i in range(pool_size)]

    def acquire(self) -> FakeConnection:
        for conn in self.connections:
            conn.in_use = True
            return conn
        raise RuntimeError("No available connections")

    def release(self, conn: FakeConnection) -> None:
        conn.in_use = False


if __name__ == "__main__":
    pool = ConnectionPool(pool_size=2)

    conn_a = pool.acquire()
    print(conn_a.execute("SELECT * FROM deals"))

    conn_b = pool.acquire()
    print(conn_b.execute("SELECT * FROM investors"))

    pool.release(conn_a)
    print("Released conn_a")