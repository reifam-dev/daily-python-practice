"""Day 138 - Consistent Hashing: Deal Shard Ring.

Places shards on a hash ring using a stable hash, so a key always
routes to the next shard clockwise (wrapping around to the first
shard past the highest point on the ring), and adding or removing a
shard only reshuffles a small fraction of keys - PCPP1 standard.
"""
from __future__ import annotations

import bisect
import hashlib


class ConsistentHashRing:
    """Distributes keys across shards on a ring, minimising rebalancing on change."""

    def __init__(self) -> None:
        self._ring: dict[int, str] = {}
        self._sorted_hashes: list[int] = []

    def _hash(self, key: str) -> int:
        """Return a stable hash, consistent across processes and restarts."""
        digest = hashlib.sha256(key.encode()).hexdigest()
        return int(digest, 16)

    def add_node(self, node_name: str) -> None:
        """Add a shard to the ring, keeping the sorted hash list in order."""
        h = self._hash(node_name)
        self._ring[h] = node_name
        bisect.insort(self._sorted_hashes, h)

    def remove_node(self, node_name: str) -> None:
        """Remove a shard from the ring, cleaning up both structures."""
        h = self._hash(node_name)
        self._sorted_hashes.remove(h)
        del self._ring[h]

    def get_node(self, key: str) -> str:
        """Return the shard responsible for this key, wrapping around the ring."""
        if not self._sorted_hashes:
            raise RuntimeError("No shards registered")

        h = self._hash(key)
        idx = bisect.bisect(self._sorted_hashes, h)
        if idx == len(self._sorted_hashes):
            idx = 0
        return self._ring[self._sorted_hashes[idx]]


if __name__ == "__main__":
    ring = ConsistentHashRing()
    ring.add_node("shard-a")
    ring.add_node("shard-b")
    ring.add_node("shard-c")

    for deal_id in ["deal-1", "deal-2", "deal-3", "deal-4"]:
        print(deal_id, "->", ring.get_node(deal_id))