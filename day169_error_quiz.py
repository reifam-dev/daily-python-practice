"""Day 169 - Read Replica Lag: Error Quiz. Find and fix three bugs."""
_primary = {}
_replica = {}
_replica_lag_writes = []


def write_to_primary(key: str, value: float) -> None:
    _primary[key] = value
    _replica_lag_writes.append((key, value))


def sync_replica() -> None:
    for key, value in _replica_lag_writes:
        _replica[key] = value


def read(key: str, from_replica: bool = True) -> float:
    if from_replica:
        return _replica[key]
    return _primary[key]


if __name__ == "__main__":
    write_to_primary("deal-1", 12_500_000.0)
    print("Immediately after write:", read("deal-1"))

    sync_replica()
    print("After sync:", read("deal-1"))