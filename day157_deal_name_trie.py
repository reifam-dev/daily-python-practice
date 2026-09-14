"""Day 157 - Trie: prefix-tree autocomplete over deal names, correctly
collecting every completed word under a prefix, not just the prefix
itself - PCPP1 standard."""
from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def _collect(self, node: TrieNode, prefix: str, results: list[str]) -> None:
        if node.is_end:
            results.append(prefix)
        for char, child in node.children.items():
            self._collect(child, prefix + char, results)

    def starts_with(self, prefix: str) -> list[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        results: list[str] = []
        self._collect(node, prefix, results)
        return results


if __name__ == "__main__":
    trie = Trie()
    for name in ["Riverside JV", "Riverside Park", "Westgate Retail"]:
        trie.insert(name)
    print(trie.starts_with("River"))