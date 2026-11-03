"""Day 196 - Percentiles by the nearest-rank method.

rank = ceil(p / 100 * n), and the answer is the value at that rank
(1-based, so index rank - 1). The caller's list is never modified
(sorted() returns a copy), and empty input or a p outside 0-100 is
rejected. Tail percentiles show what an average hides - PCPP1 standard.
"""
from __future__ import annotations

import math


def percentile(values: list[float], p: float) -> float:
    """The p-th percentile of values, nearest-rank method."""
    if not values:
        raise ValueError("values must not be empty")
    if not 0 <= p <= 100:
        raise ValueError("p must be between 0 and 100")
    ordered = sorted(values)
    rank = max(1, math.ceil(p * len(ordered) / 100))
    return ordered[rank - 1]


if __name__ == "__main__":
    latencies_ms = [120, 95, 180, 110, 3000, 105, 130, 99, 101, 115]
    print(percentile(latencies_ms, 50))
    print(latencies_ms)
    print(percentile(latencies_ms, 95))
    print(percentile(latencies_ms, 100))
    print(sum(latencies_ms) / len(latencies_ms))