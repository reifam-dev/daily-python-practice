"""Day 169 - Read Replica Lag: reads default to the replica for
scalability, but a caller can request read-your-writes consistency
by reading from the primary right after their own write, since the
replica may not have synced yet - PCPP1 standard."""
from __future__ import annotations

_primary: dict[str, float] = {}
_replica: dict[str, float] = {}
_replica_lag_writes: list[tuple[str, float]] = []


def write_to_primary(key: str, value: float) -> None:
    _primary[key] = value
    _replica_lag_writes.append((key, value))


def sync_replica() -> None:
    """Simulates asynchronous replication catching up."""
    for key, value in _replica_lag_writes:
        _replica[key] = value
    _replica_lag_writes.clear()


def read(key: str, from_replica: bool = True) -> float | None:
    """Read from the replica by default (scalable), or the primary
    for guaranteed read-your-writes consistency."""
    store = _replica if from_replica else _primary
    return store.get(key)


if __name__ == "__main__":
    write_to_primary("deal-1", 12_500_000.0)
    print("Replica immediately after write:", read("deal-1", from_replica=True))   # None - not synced yet
    print("Primary immediately after write:", read("deal-1", from_replica=False))  # 12500000.0

    sync_replica()
    print("Replica after sync:", read("deal-1", from_replica=True))  # 12500000.0