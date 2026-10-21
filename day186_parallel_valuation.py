"""Day 186 - Thread Pool Fan-Out: valuing many deals concurrently.

The pool is used as a context manager so its threads are always shut
down, results are collected as they complete under an overall timeout,
and each task's failure is captured per deal instead of aborting the
whole batch and discarding the successes - PCPP1 standard.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed


def value_deal(deal_id: str) -> float:
    """Simulate a valuation call that can fail for some deals."""
    if deal_id == "deal-3":
        raise ValueError(f"No valuation data for {deal_id}")
    return len(deal_id) * 1_000_000.0


def value_all(
    deal_ids: list[str], timeout: float = 5.0
) -> tuple[dict[str, float], dict[str, str]]:
    """Return (results, errors), keyed by deal id."""
    results: dict[str, float] = {}
    errors: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_id = {executor.submit(value_deal, d): d for d in deal_ids}
        for future in as_completed(future_to_id, timeout=timeout):
            deal_id = future_to_id[future]
            try:
                results[deal_id] = future.result()
            except ValueError as exc:
                errors[deal_id] = str(exc)
    return dict(sorted(results.items())), errors


if __name__ == "__main__":
    print(value_all(["deal-1", "deal-2"]))
    print(value_all(["deal-1", "deal-3", "deal-2"]))