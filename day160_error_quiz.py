"""Day 160 - Rolling Hash: Error Quiz. Find and fix three bugs."""
BASE = 256
MOD = 1_000_000_007


def compute_hash(s: str) -> int:
    h = 0
    for char in s:
        h = h * BASE + ord(char)
    return h


def roll_hash(old_hash: int, old_char: str, new_char: str, window_size: int) -> int:
    h = old_hash - ord(old_char) * BASE ** window_size
    h = h * BASE + ord(new_char)
    return h


def find_pattern(text: str, pattern: str) -> list:
    n, m = len(text), len(pattern)
    pattern_hash = compute_hash(pattern)
    matches = []

    window_hash = compute_hash(text[0:m])
    for i in range(n - m):
        if window_hash == pattern_hash:
            matches.append(i)
        window_hash = roll_hash(window_hash, text[i], text[i + m], m)

    return matches


if __name__ == "__main__":
    print(find_pattern("abracadabra", "abra"))