"""Day 152 - LRU Cache: uses OrderedDict to track true access recency
- both get() and put() move an entry to the "most recently used" end,
so eviction always removes the genuinely least-recently-used key -
PCPP1 standard."""
from __future__ import annotations
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._cache: OrderedDict = OrderedDict()

    def get(self, key: str):
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: str, value) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)


if __name__ == "__main__":
    cache = LRUCache(capacity=2)
    cache.put("deal-1", "Riverside JV")
    cache.put("deal-2", "Westgate Retail")
    cache.get("deal-1")  # deal-1 is now most recently used
    cache.put("deal-3", "Logistics Portfolio")  # evicts deal-2, not deal-1

    print(cache.get("deal-1"))  # Riverside JV
    print(cache.get("deal-2"))  # None, evicted
    print(cache.get("deal-3"))  # Logistics Portfolio