"""Day 160 - Rolling Hash: computes a substring hash in O(1) as the
window slides, by subtracting the outgoing character's contribution
and adding the incoming one, rather than recomputing from scratch -
PCPP1 standard. Uses modular arithmetic to keep hashes bounded."""
from __future__ import annotations

_BASE = 256
_MOD = 1_000_000_007


def compute_hash(s: str) -> int:
    h = 0
    for char in s:
        h = (h * _BASE + ord(char)) % _MOD
    return h


def roll_hash(old_hash: int, old_char: str, new_char: str, window_size: int) -> int:
    high_order = pow(_BASE, window_size - 1, _MOD)
    h = (old_hash - ord(old_char) * high_order) % _MOD
    h = (h * _BASE + ord(new_char)) % _MOD
    return h


def find_pattern(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m > n:
        return []

    pattern_hash = compute_hash(pattern)
    matches: list[int] = []

    window_hash = compute_hash(text[0:m])
    for i in range(n - m + 1):
        if window_hash == pattern_hash and text[i:i + m] == pattern:
            matches.append(i)
        if i < n - m:
            window_hash = roll_hash(window_hash, text[i], text[i + m], m)

    return matches


if __name__ == "__main__":
    print(find_pattern("abracadabra", "abra"))  # [0, 7]