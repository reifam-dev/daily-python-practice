"""Day 172 - Cache Invalidation: reads check the entry's TTL and
treat an expired entry as a miss, actively removing it too - rather
than serving stale data just because it's technically still sitting
in the dict - PCPP1 standard."""
from __future__ import annotations
import time

_cache: dict[str, object] = {}
_cache_timestamps: dict[str, float] = {}
_TTL_SECONDS = 5.0


def cache_get(key: str):
    """Return the value if present and not expired; otherwise None."""
    if key not in _cache:
        return None

    age = time.time() - _cache_timestamps[key]
    if age > _TTL_SECONDS:
        invalidate(key)
        return None

    return _cache[key]


def cache_set(key: str, value) -> None:
    _cache[key] = value
    _cache_timestamps[key] = time.time()


def invalidate(key: str) -> None:
    _cache.pop(key, None)
    _cache_timestamps.pop(key, None)


if __name__ == "__main__":
    cache_set("deal-1", 12_500_000.0)
    print(cache_get("deal-1"))

    time.sleep(0.1)
    print(cache_get("deal-1"))

    invalidate("deal-1")
    print(cache_get("deal-1"))