"""Day 151 - Bloom Filters: a space-efficient probabilistic set. A
"might contain" of False is a guaranteed absence; True can be a false
positive but never a false negative - PCPP1 standard."""
from __future__ import annotations
import hashlib


class BloomFilter:
    def __init__(self, size: int, num_hashes: int) -> None:
        if size <= 0 or num_hashes <= 0:
            raise ValueError("size and num_hashes must be positive")
        self.size = size
        self.num_hashes = num_hashes
        self._bits = [0] * size

    def _hashes(self, item: str):
        for i in range(self.num_hashes):
            digest = hashlib.sha256(f"{item}{i}".encode()).hexdigest()
            yield int(digest, 16) % self.size

    def add(self, item: str) -> None:
        for h in self._hashes(item):
            self._bits[h] = 1

    def might_contain(self, item: str) -> bool:
        return all(self._bits[h] == 1 for h in self._hashes(item))


if __name__ == "__main__":
    bf = BloomFilter(size=1000, num_hashes=3)
    bf.add("Riverside JV")
    bf.add("Westgate Retail")

    print(bf.might_contain("Riverside JV"))       # True
    print(bf.might_contain("Logistics Portfolio"))  # False (not added)