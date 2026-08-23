"""Day 135 - Read-Through and Write-Through Caching: Error Quiz.

Find and fix three bugs. No location hints.
"""
_database = {
    "deal-1": {"deal_name": "Riverside JV", "market_value": 12_500_000.0},
}
_cache = {}


def get_deal(deal_id: str) -> dict:
    if deal_id in _cache:
        print(f"cache hit: {deal_id}")
        return _cache[deal_id]

    print(f"cache miss: {deal_id}")
    deal = _database.get(deal_id)
    return deal


def update_deal(deal_id: str, new_market_value: float) -> None:
    _database[deal_id]["market_value"] = new_market_value


if __name__ == "__main__":
    print(get_deal("deal-1"))
    print(get_deal("deal-1"))

    update_deal("deal-1", 13_000_000.0)
    print(get_deal("deal-1"))