"""Day 153 - Binary Search: O(log n) search over sorted data, with
low/high bounds and midpoint advancement that provably terminate -
PCPP1 standard."""
from __future__ import annotations


def binary_search(sorted_list: list, target) -> int:
    low, high = 0, len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


if __name__ == "__main__":
    deals = [10, 20, 30, 40, 50, 60, 70]
    print(binary_search(deals, 40))  # 3
    print(binary_search(deals, 25))  # -1