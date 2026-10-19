"""Day 183 - Top-K with a Heap.

To keep the K LARGEST values, hold a MIN-heap of size K: the root is
the smallest of the current top K, so it is the one to evict when a
bigger value arrives. An insertion index breaks ties so two equal
values never force Python to compare the deal dicts themselves (it is
negated so the EARLIER deal wins a tie), and the result is sorted
largest-first - PCPP1 standard.
"""
from __future__ import annotations

import heapq


def top_k_deals(deals: list[dict], k: int) -> list[dict]:
    """Return the k deals with the highest market_value, largest first."""
    if k <= 0:
        return []

    heap: list[tuple[float, int, dict]] = []
    for index, deal in enumerate(deals):
        heapq.heappush(heap, (deal["market_value"], -index, deal))
        if len(heap) > k:
            heapq.heappop(heap)
    return [deal for _, _, deal in sorted(heap, reverse=True)]


if __name__ == "__main__":
    deals = [
        {"name": "Riverside JV", "market_value": 12_500_000.0},
        {"name": "Westgate Retail", "market_value": 8_100_000.0},
        {"name": "Logistics Portfolio", "market_value": 34_200_000.0},
        {"name": "Docklands", "market_value": 15_750_000.0},
    ]
    print([d["name"] for d in top_k_deals(deals, 2)])

    tied = deals + [{"name": "Midtown", "market_value": 12_500_000.0}]
    print([d["name"] for d in top_k_deals(tied, 3)])