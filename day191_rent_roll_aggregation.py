"""Day 191 - Rent Roll Aggregation: group-by with accumulation.

Rent is ADDED to its sector's running total (dict.get with a default),
never assigned over it. Shares are each sector's rent over the GRAND
total, and the result is ordered largest sector first - PCPP1 standard.
"""
from __future__ import annotations


def rent_by_sector(leases: list[dict]) -> dict[str, float]:
    """Total annual rent per sector, largest first."""
    totals: dict[str, float] = {}
    for lease in leases:
        sector = lease["sector"]
        totals[sector] = totals.get(sector, 0.0) + lease["annual_rent"]
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def share_of_total(totals: dict[str, float]) -> dict[str, float]:
    """Each sector's percentage of the grand total."""
    grand_total = sum(totals.values())
    if grand_total <= 0:
        raise ValueError("grand total must be positive")
    return {sector: round(rent / grand_total * 100, 1) for sector, rent in totals.items()}


if __name__ == "__main__":
    leases = [
        {"tenant": "Acme Logistics", "sector": "logistics", "annual_rent": 250_000.0},
        {"tenant": "Beta Retail", "sector": "retail", "annual_rent": 120_000.0},
        {"tenant": "Gamma Office", "sector": "office", "annual_rent": 180_000.0},
        {"tenant": "Delta Logistics", "sector": "logistics", "annual_rent": 90_000.0},
        {"tenant": "Epsilon Retail", "sector": "retail", "annual_rent": 60_000.0},
    ]
    totals = rent_by_sector(leases)
    print(totals)
    print(share_of_total(totals))