"""Day 158 - Union-Find: groups items into connected clusters (e.g.
deals that share an investor, transitively) using path compression so
repeated find() calls stay fast as the structure grows -
PCPP1 standard."""
from __future__ import annotations


class UnionFind:
    def __init__(self, items: list) -> None:
        self.parent = {item: item for item in items}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # path compression
        return self.parent[item]

    def union(self, a, b) -> None:
        root_a, root_b = self.find(a), self.find(b)
        if root_a != root_b:
            self.parent[root_a] = root_b

    def connected(self, a, b) -> bool:
        return self.find(a) == self.find(b)


if __name__ == "__main__":
    uf = UnionFind(["deal-1", "deal-2", "deal-3", "deal-4"])
    uf.union("deal-1", "deal-2")
    uf.union("deal-2", "deal-3")

    print(uf.connected("deal-1", "deal-3"))  # True
    print(uf.connected("deal-1", "deal-4"))  # False