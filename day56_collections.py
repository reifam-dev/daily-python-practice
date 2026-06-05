# Day 56 - Clean collections module examples
# New concepts: defaultdict, Counter, deque, OrderedDict
# PEP 8, docstrings, type hints, exceptions throughout

from collections import defaultdict, Counter, deque
from typing import List, Dict


def word_frequency(words: List[str]) -> Dict[str, int]:
    """Count word frequencies using defaultdict.

    defaultdict(int) returns 0 for missing keys automatically —
    no need to check if key exists before incrementing.
    """
    frequency: Dict[str, int] = defaultdict(int)
    for word in words:
        frequency[word] += 1
    return dict(frequency)


def group_by_first_letter(words: List[str]) -> Dict[str, List[str]]:
    """Group words by their first letter using defaultdict(list).

    defaultdict(list) returns [] for missing keys automatically.
    """
    groups: Dict[str, List[str]] = defaultdict(list)
    for word in words:
        if word:
            groups[word[0].lower()].append(word)
    return dict(groups)


def analyse_text(text: str) -> None:
    """Analyse character and word frequency using Counter."""
    char_count = Counter(text.lower().replace(" ", ""))
    word_count = Counter(text.lower().split())

    print(f"  Top 5 characters : {char_count.most_common(5)}")
    print(f"  Top 3 words      : {word_count.most_common(3)}")
    print(f"  Total chars      : {sum(char_count.values())}")
    print(f"  Unique chars     : {len(char_count)}")


if __name__ == "__main__":
    print("=== defaultdict(int) — word frequency ===\n")
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    freq = word_frequency(words)
    print(f"  Frequencies : {freq}\n")

    print("=== defaultdict(list) — group by first letter ===\n")
    animals = ["Ant", "Bear", "Bee", "Cat", "Crane", "Dog", "Duck"]
    groups = group_by_first_letter(animals)
    for letter, group in sorted(groups.items()):
        print(f"  {letter}: {group}")

    print("\n=== Counter ===\n")
    analyse_text("the quick brown fox jumps over the lazy dog the fox")

    c1 = Counter({"apple": 3, "banana": 2})
    c2 = Counter({"apple": 1, "cherry": 4})
    print(f"\n  c1 + c2          : {c1 + c2}")
    print(f"  c1 - c2          : {c1 - c2}")
    print(f"  c1['missing']    : {c1['missing']}")

    print("\n=== deque — fixed-size sliding window ===\n")
    window: deque = deque(maxlen=3)
    for i in range(1, 7):
        window.append(i)
        print(f"  Added {i} → window: {list(window)}")

    print("\n=== deque — browser history (appendleft) ===\n")
    history: deque = deque()
    for page in ["home", "about", "contact", "shop"]:
        history.appendleft(page)
    print(f"  History (newest first): {list(history)}")
    print(f"  Current page          : {history[0]}")
    print(f"  Back one page         : {history[1]}")