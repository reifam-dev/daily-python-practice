"""Day 172 - Cache Invalidation: Error Quiz. Find and fix three bugs."""
import time

_cache = {}
_cache_timestamps = {}
TTL_SECONDS = 5.0


def cache_get(key: str):
    if key in _cache:
        return _cache[key]
    return None


def cache_set(key: str, value) -> None:
    _cache[key] = value
    _cache_timestamps[key] = time.time()


def invalidate(key: str) -> None:
    if key in _cache:
        del _cache[key]


if __name__ == "__main__":
    cache_set("deal-1", 12_500_000.0)
    print(cache_get("deal-1"))

    time.sleep(0.1)
    print(cache_get("deal-1"))

    invalidate("deal-1")
    print(cache_get("deal-1"))