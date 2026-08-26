"""Day 137 - Sharding and Partition Key Selection: Error Quiz.

Find and fix three bugs. No location hints.
"""
NUM_SHARDS = 4


class ShardedStore:
    def __init__(self, num_shards: int):
        self.num_shards = num_shards
        self.shards = [{} for _ in range(num_shards)]

    def _shard_for_key(self, key: str) -> int:
        return hash(key) % self.num_shards

    def put(self, key: str, value: dict) -> None:
        shard_index = self._shard_for_key(key)
        self.shards[shard_index][key] = value

    def get(self, key: str) -> dict:
        shard_index = self._shard_for_key(key)
        return self.shards[shard_index].get(key)

    def shard_sizes(self) -> list[int]:
        return [len(shard) for shard in self.shards]


if __name__ == "__main__":
    store = ShardedStore(NUM_SHARDS)

    for i in range(20):
        deal_id = f"deal-{i}"
        store.put(deal_id, {"deal_name": f"Deal {i}", "market_value": 1_000_000.0 * i})

    print("Shard sizes:", store.shard_sizes())
    print("deal-7:", store.get("deal-7"))