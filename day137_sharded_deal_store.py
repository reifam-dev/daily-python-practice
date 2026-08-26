"""Day 137 - Sharding and Partition Key Selection: Sharded Deal Store.

Distributes records across a fixed number of shards using a stable
hash of the partition key, so the same key always routes to the same
shard - PCPP1 standard.
"""
from __future__ import annotations

import hashlib

_NUM_SHARDS = 4


class ShardedStore:
    """Distributes records across a fixed number of shards by key hash."""

    def __init__(self, num_shards: int) -> None:
        if num_shards < 1:
            raise ValueError("num_shards must be at least 1")
        self.num_shards = num_shards
        self.shards: list[dict] = [{} for _ in range(num_shards)]

    def _shard_for_key(self, key: str) -> int:
        """Return a stable shard index for a given key, consistent across runs."""
        digest = hashlib.sha256(key.encode()).hexdigest()
        return int(digest, 16) % self.num_shards

    def put(self, key: str, value: dict) -> None:
        shard_index = self._shard_for_key(key)
        self.shards[shard_index][key] = value

    def get(self, key: str) -> dict | None:
        shard_index = self._shard_for_key(key)
        return self.shards[shard_index].get(key)

    def shard_sizes(self) -> list[int]:
        return [len(shard) for shard in self.shards]


if __name__ == "__main__":
    store = ShardedStore(_NUM_SHARDS)

    for i in range(20):
        deal_id = f"deal-{i}"
        store.put(deal_id, {"deal_name": f"Deal {i}", "market_value": 1_000_000.0 * i})

    print("Shard sizes:", store.shard_sizes())
    print("deal-7:", store.get("deal-7"))