"""Day 163 - Materialized Views: Error Quiz. Find and fix three bugs."""
_deals = {
    "deal-1": {"region": "London", "market_value": 12_500_000.0},
    "deal-2": {"region": "Midlands", "market_value": 34_200_000.0},
    "deal-3": {"region": "London", "market_value": 8_100_000.0},
}

_region_totals_view = {}


def refresh_region_totals() -> None:
    totals = {}
    for deal in _deals.values():
        region = deal["region"]
        totals[region] = deal["market_value"]
    _region_totals_view = totals


def get_region_total(region: str) -> float:
    return _region_totals_view.get(region, 0.0)


if __name__ == "__main__":
    refresh_region_totals()
    print(get_region_total("London"))
    print(get_region_total("Midlands"))