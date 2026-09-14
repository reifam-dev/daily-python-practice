"""Day 157 - Trie: Error Quiz. Find and fix three bugs."""
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode
            node = node.children[char]
        node.is_end = True

    def starts_with(self, prefix: str) -> list:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return [prefix]


if __name__ == "__main__":
    trie = Trie()
    for name in ["Riverside JV", "Riverside Park", "Westgate Retail"]:
        trie.insert(name)
    print(trie.starts_with("River"))