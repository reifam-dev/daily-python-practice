# Day 57 - Clean itertools module examples
# New concepts: chain, product, combinations, permutations, islice, groupby, cycle
# PEP 8, docstrings, type hints, exceptions throughout

import itertools
from typing import List, Tuple


if __name__ == "__main__":
    print("=== itertools.chain ===\n")
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    list3 = [7, 8, 9]
    combined = list(itertools.chain(list1, list2, list3))
    print(f"  chain result : {combined}\n")

    print("=== itertools.product — cartesian product ===\n")
    colours = ["red", "blue"]
    sizes = ["S", "M", "L"]
    variants: List[Tuple] = list(itertools.product(colours, sizes))
    print(f"  Variants ({len(variants)}):")
    for v in variants:
        print(f"    {v}")

    print("\n=== itertools.combinations ===\n")
    items = ["A", "B", "C", "D"]
    for r in [2, 3]:
        combos = list(itertools.combinations(items, r))
        print(f"  C({len(items)},{r}) = {len(combos)} : {combos}")

    print("\n=== itertools.permutations ===\n")
    for r in [2, 3]:
        perms = list(itertools.permutations(items, r))
        print(f"  P({len(items)},{r}) = {len(perms)} : {perms[:4]}...")

    print("\n=== itertools.accumulate ===\n")
    numbers = [1, 2, 3, 4, 5]
    running_sum = list(itertools.accumulate(numbers))
    running_product = list(itertools.accumulate(numbers, lambda a, b: a * b))
    print(f"  Running sum     : {running_sum}")
    print(f"  Running product : {running_product}")

    print("\n=== itertools.islice ===\n")
    first_five = list(itertools.islice(range(100), 5))
    middle_five = list(itertools.islice(range(100), 10, 15))
    print(f"  First 5    : {first_five}")
    print(f"  Items 10-14: {middle_five}")

    print("\n=== itertools.groupby ===\n")
    data = [1, 1, 2, 2, 2, 3, 1, 1]
    for key, group in itertools.groupby(data):
        items_in_group = list(group)  # must consume immediately
        print(f"  key={key} → {items_in_group}")

    print("\n=== itertools.cycle (safe with islice) ===\n")
    colours_cycle = itertools.cycle(["red", "green", "blue"])
    first_eight = list(itertools.islice(colours_cycle, 8))
    print(f"  First 8 from cycle: {first_eight}")