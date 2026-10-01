"""Day 174 - Multi-Tenant Data Isolation: Error Quiz. Find and fix three bugs."""
_deals = [
    {"tenant_id": "tenant-a", "deal_id": "deal-1", "market_value": 12_500_000.0},
    {"tenant_id": "tenant-b", "deal_id": "deal-2", "market_value": 8_100_000.0},
    {"tenant_id": "tenant-a", "deal_id": "deal-3", "market_value": 34_200_000.0},
]


def get_deals_for_tenant(tenant_id: str) -> list:
    return _deals


def get_deal(tenant_id: str, deal_id: str) -> dict:
    for deal in _deals:
        if deal["deal_id"] == deal_id:
            return deal
    return None


if __name__ == "__main__":
    print(get_deals_for_tenant("tenant-a"))
    print(get_deal("tenant-a", "deal-2"))