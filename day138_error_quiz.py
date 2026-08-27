"""Day 138 - Consistent Hashing: Error Quiz.

Find and fix three bugs. No location hints.
"""
import bisect
import hashlib


class ConsistentHashRing:
    def __init__(self):
        self._ring = {}
        self._sorted_hashes = []

    def _hash(self, key: str) -> int:
        digest = hashlib.sha256(key.encode()).hexdigest()
        return int(digest, 16)

    def add_node(self, node_name: str) -> None:
        h = self._hash(node_name)
        self._ring[h] = node_name
        self._sorted_hashes.append(h)

    def remove_node(self, node_name: str) -> None:
        h = self._hash(node_name)
        self._sorted_hashes.remove(h)

    def get_node(self, key: str) -> str:
        h = self._hash(key)
        idx = bisect.bisect(self._sorted_hashes, h)
        return self._ring[self._sorted_hashes[idx]]


if __name__ == "__main__":
    ring = ConsistentHashRing()
    ring.add_node("shard-a")
    ring.add_node("shard-b")
    ring.add_node("shard-c")

    for deal_id in ["deal-1", "deal-2", "deal-3", "deal-4"]:
        print(deal_id, "->", ring.get_node(deal_id))