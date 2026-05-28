# Day 48 - Clean Proxy pattern
# New concepts: Proxy pattern, lazy initialisation, access control, logging proxy
# PEP 8, docstrings, type hints, exceptions throughout

from abc import ABC, abstractmethod
from typing import List, Optional


class Database(ABC):
    """Abstract interface shared by RealDatabase and all proxies."""

    @abstractmethod
    def query(self, sql: str) -> str:
        """Execute a query and return the result."""
        pass


class RealDatabase(Database):
    """The real heavyweight object — expensive to create."""

    def __init__(self, name: str) -> None:
        print(f"  [RealDatabase] Connecting to '{name}'...")
        self._name = name

    def query(self, sql: str) -> str:
        return f"[{self._name}] Result: {sql}"


class VirtualProxy(Database):
    """Virtual proxy — delays creation of RealDatabase until first use.

    Lazy initialisation — the real object is only created when needed.
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._real: Optional[RealDatabase] = None

    def query(self, sql: str) -> str:
        """Create RealDatabase on first call, reuse on subsequent calls."""
        if self._real is None:
            self._real = RealDatabase(self._name)
        return self._real.query(sql)


class ProtectionProxy(Database):
    """Protection proxy — controls access based on allowed users."""

    def __init__(self, name: str, allowed_users: List[str]) -> None:
        self._name = name
        self._allowed_users = allowed_users
        self._real: Optional[RealDatabase] = None

    def query(self, sql: str, user: str = "anonymous") -> str:
        """Allow query only if user is in allowed list."""
        if user not in self._allowed_users:
            raise PermissionError(
                f"User '{user}' is not authorised to query '{self._name}'."
            )
        if self._real is None:
            self._real = RealDatabase(self._name)
        return self._real.query(sql)


class LoggingProxy(Database):
    """Logging proxy — records all queries and their results."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._real: Optional[RealDatabase] = None
        self._log: List[dict] = []

    def query(self, sql: str) -> str:
        """Execute query and log both the SQL and result."""
        if self._real is None:
            self._real = RealDatabase(self._name)
        result = self._real.query(sql)
        self._log.append({"sql": sql, "result": result})
        return result

    def get_log(self) -> List[dict]:
        """Return a copy of the query log."""
        return self._log.copy()


if __name__ == "__main__":
    print("=== VirtualProxy — lazy initialisation ===\n")
    proxy = VirtualProxy("ProductionDB")
    print("  Proxy created — no connection yet")
    print(f"  {proxy.query('SELECT * FROM users')}")
    print(f"  {proxy.query('SELECT * FROM orders')}")

    print("\n=== ProtectionProxy — access control ===\n")
    protected = ProtectionProxy("HRDatabase", ["alice", "bob"])
    try:
        print(f"  {protected.query('SELECT * FROM salaries', user='alice')}")
        print(f"  {protected.query('SELECT * FROM salaries', user='charlie')}")
    except PermissionError as e:
        print(f"  Error: {e}")

    print("\n=== LoggingProxy — audit trail ===\n")
    logged = LoggingProxy("AuditDB")
    logged.query("SELECT * FROM transactions")
    logged.query("SELECT * FROM accounts")
    print("  Query log:")
    for entry in logged.get_log():
        print(f"    SQL: {entry['sql']}")
        print(f"    Result: {entry['result']}")