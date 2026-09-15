"""Day 158 - Union-Find: Error Quiz. Find and fix three bugs."""
class UnionFind:
    def __init__(self, items: list):
        self.parent = {item: item for item in items}

    def find(self, item):
        if self.parent[item] != item:
            return self.find(self.parent[item])
        return item

    def union(self, a, b) -> None:
        self.parent[a] = b

    def connected(self, a, b) -> bool:
        return self.find(a) == self.find(b)


if __name__ == "__main__":
    uf = UnionFind(["deal-1", "deal-2", "deal-3", "deal-4"])
    uf.union("deal-1", "deal-2")
    uf.union("deal-2", "deal-3")

    print(uf.connected("deal-1", "deal-3"))
    print(uf.connected("deal-1", "deal-4"))