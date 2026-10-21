"""Day 186 - Thread Pool Fan-Out: Error Quiz. Find and fix three bugs."""
from concurrent.futures import ThreadPoolExecutor


def value_deal(deal_id: str) -> float:
    if deal_id == "deal-3":
        raise ValueError(f"No valuation data for {deal_id}")
    return len(deal_id) * 1_000_000.0


def value_all(deal_ids: list) -> dict:
    results = {}
    executor = ThreadPoolExecutor(max_workers=3)
    futures = {deal_id: executor.submit(value_deal, deal_id) for deal_id in deal_ids}
    for deal_id, future in futures.items():
        results[deal_id] = future.result()
    return results


if __name__ == "__main__":
    print(value_all(["deal-1", "deal-2"]))
    try:
        print(value_all(["deal-1", "deal-3", "deal-2"]))
    except ValueError as exc:
        print(f"Whole batch lost: {exc}")