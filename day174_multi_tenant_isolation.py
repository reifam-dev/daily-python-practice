"""Day 174 - Multi-Tenant Data Isolation: every query filters by
tenant_id, so tenant A can never see or fetch tenant B's records,
even by directly requesting a known deal_id that happens to belong
to another tenant - PCPP1 standard."""
from __future__ import annotations

_deals: list[dict] = [
    {"tenant_id": "tenant-a", "deal_id": "deal-1", "market_value": 12_500_000.0},
    {"tenant_id": "tenant-b", "deal_id": "deal-2", "market_value": 8_100_000.0},
    {"tenant_id": "tenant-a", "deal_id": "deal-3", "market_value": 34_200_000.0},
]


def get_deals_for_tenant(tenant_id: str) -> list[dict]:
    return [deal for deal in _deals if deal["tenant_id"] == tenant_id]


def get_deal(tenant_id: str, deal_id: str) -> dict | None:
    for deal in _deals:
        if deal["deal_id"] == deal_id and deal["tenant_id"] == tenant_id:
            return deal
    return None


if __name__ == "__main__":
    print(get_deals_for_tenant("tenant-a"))       # only tenant-a's 2 deals
    print(get_deal("tenant-a", "deal-2"))         # None - deal-2 belongs to tenant-b