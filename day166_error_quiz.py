"""Day 166 - Write-Ahead Logging: Error Quiz. Find and fix three bugs."""
_data_store = {}
_wal = []


def write(key: str, value: float) -> None:
    _data_store[key] = value
    _wal.append((key, value))


def crash_and_recover() -> dict:
    recovered_store = {}
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