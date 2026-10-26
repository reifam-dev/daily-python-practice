"""Day 190 - WALE: Weighted Average Lease Expiry.

Each lease's remaining term is weighted by its ANNUAL RENT, so the
result is divided by TOTAL RENT (not by the number of leases). A lease
already past expiry has no remaining term, so it counts as 0 years
rather than a negative number - PCPP1 standard.
"""
from __future__ import annotations


def wale(leases: list[tuple[float, float]]) -> float:
    """WALE in years, from (annual_rent, years_remaining) pairs."""
    total_rent = sum(rent for rent, _ in leases)
    if total_rent <= 0:
        raise ValueError("total rent must be positive")
    weighted = sum(rent * max(years, 0.0) for rent, years in leases)
    return weighted / total_rent


if __name__ == "__main__":
    leases = [(250_000.0, 4.0), (180_000.0, 3.0), (90_000.0, 1.0), (60_000.0, -0.5)]
    print(round(wale(leases), 2))
    try:
        wale([])
    except ValueError as exc:
        print(f"Rejected: {exc}")