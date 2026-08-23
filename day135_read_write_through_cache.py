"""Day 135 - Read-Through and Write-Through Caching: Deal Cache.

Read-through: a cache miss transparently fetches from the underlying
store and populates the cache before returning. Write-through: a
write updates the store and the cache together, atomically from the
caller's perspective, so the two never drift apart - PCPP1 standard.
"""
from __future__ import annotations

_database: dict[str, dict] = {
    "deal-1": {"deal_name": "Riverside JV", "market_value": 12_500_000.0},
}
_cache: dict[str, dict] = {}


def get_deal(deal_id: str) -> dict | None:
    """Read-through: serve from cache if present, else fetch and populate it."""
    if deal_id in _cache:
        print(f"cache hit: {deal_id}")
        return _cache[deal_id]

    print(f"cache miss: {deal_id}")
    deal = _database.get(deal_id)
    if deal is not None:
        _cache[deal_id] = deal
    return deal


def update_deal(deal_id: str, new_market_value: float) -> None:
    """Write-through: update the database and the cache together."""
    if deal_id not in _database:
        raise KeyError(f"No such deal: {deal_id}")

    _database[deal_id]["market_value"] = new_market_value
    _cache[deal_id] = dict(_database[deal_id])


if __name__ == "__main__":
    print(get_deal("deal-1"))  # miss, populates cache
    print(get_deal("deal-1"))  # hit, served from cache

    update_deal("deal-1", 13_000_000.0)
    print(get_deal("deal-1"))  # hit, and reflects the update immediately