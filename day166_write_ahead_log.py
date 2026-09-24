"""Day 166 - Write-Ahead Logging: the log entry is appended before (or
atomically with) the in-memory state update, so that even after a
total loss of in-memory state, replaying the log from the start
reconstructs exactly what was there before the crash -
PCPP1 standard."""
from __future__ import annotations

_data_store: dict[str, float] = {}
_wal: list[tuple[str, float]] = []


def write(key: str, value: float) -> None:
    """Log the write first (durability guarantee), then apply it."""
    _wal.append((key, value))
    _data_store[key] = value


def crash_and_recover() -> dict[str, float]:
    """Rebuild state purely by replaying the log in order - the log is
    the source of truth, not the in-memory store, which is why this
    works even after _data_store is completely wiped."""
    recovered_store: dict[str, float] = {}
    for key, value in _wal:
        recovered_store[key] = value
    return recovered_store


if __name__ == "__main__":
    write("deal-1", 12_500_000.0)
    write("deal-2", 34_200_000.0)

    print("Live store:", _data_store)

    _data_store.clear()
    print("After crash:", _data_store)

    recovered = crash_and_recover()
    print("Recovered:", recovered)
    assert recovered == {"deal-1": 12_500_000.0, "deal-2": 34_200_000.0}