"""Day 152 - LRU Cache: Error Quiz. Find and fix three bugs."""
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

    def get(self, key: str):
        if key not in self.cache:
            return None
        return self.cache[key]

    def put(self, key: str, value) -> None:
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            oldest_key = list(self.cache.keys())[0]
            del self.cache[oldest_key]


if __name__ == "__main__":
    cache = LRUCache(capacity=2)
    cache.put("deal-1", "Riverside JV")
    cache.put("deal-2", "Westgate Retail")
    cache.get("deal-1")
    cache.put("deal-3", "Logistics Portfolio")

    print(cache.get("deal-1"))
    print(cache.get("deal-2"))
    print(cache.get("deal-3"))