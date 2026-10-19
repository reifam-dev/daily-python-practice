"""Day 183 - Top-K with a Heap: Error Quiz. Find and fix three bugs."""
import heapq


def top_k_deals(deals: list, k: int) -> list:
    heap = []
    for deal in deals:
        heapq.heappush(heap, (-deal["market_value"], deal))
        if len(heap) > k:
            heapq.heappop(heap)
    return [deal for _, deal in heap]


if __name__ == "__main__":
    deals = [
        {"name": "Riverside JV", "market_value": 12_500_000.0},
        {"name": "Westgate Retail", "market_value": 8_100_000.0},
        {"name": "Logistics Portfolio", "market_value": 34_200_000.0},
        {"name": "Docklands", "market_value": 15_750_000.0},
    ]
    print([d["name"] for d in top_k_deals(deals, 2)])

    tied = deals + [{"name": "Midtown", "market_value": 12_500_000.0}]
    try:
        print([d["name"] for d in top_k_deals(tied, 2)])
    except TypeError as exc:
        print(f"Crashed: {exc}")