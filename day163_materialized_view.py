"""Day 163 - Materialized Views: a precomputed, denormalised summary
table refreshed on demand, so an expensive aggregation query only
needs to run once per refresh rather than on every read -
PCPP1 standard."""
from __future__ import annotations

_deals: dict[str, dict] = {
    "deal-1": {"region": "London", "market_value": 12_500_000.0},
    "deal-2": {"region": "Midlands", "market_value": 34_200_000.0},
    "deal-3": {"region": "London", "market_value": 8_100_000.0},
}

_region_totals_view: dict[str, float] = {}


def refresh_region_totals() -> None:
    """Recompute the materialized view from the source of truth."""
    global _region_totals_view
    totals: dict[str, float] = {}
    for deal in _deals.values():
        region = deal["region"]
        totals[region] = totals.get(region, 0.0) + deal["market_value"]
    _region_totals_view = totals


def get_region_total(region: str) -> float:
    """Read from the view - fast, but only as fresh as the last refresh."""
    return _region_totals_view.get(region, 0.0)


if __name__ == "__main__":
    refresh_region_totals()
    print(get_region_total("London"))    # 20,600,000.0
    print(get_region_total("Midlands"))  # 34,200,000.0