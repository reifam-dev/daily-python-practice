"""Day 130 - Optimistic Locking: Version-Controlled Deal Updates.

Each deal carries a version number. An update must supply the version
it last read; if another writer has since changed the record (version
no longer matches), the update is rejected rather than silently
overwriting the other writer's change - PCPP1 standard.
"""
from __future__ import annotations

_DEALS: dict[str, dict] = {
    "deal-1": {"deal_name": "Riverside JV", "market_value": 12_500_000.0, "version": 1},
}


class StaleVersionError(Exception):
    """Raised when an update's expected version no longer matches the stored record."""


def update_deal(deal_id: str, expected_version: int, new_market_value: float) -> dict:
    """Update a deal's market value, rejecting the write if the version is stale."""
    deal = _DEALS[deal_id]

    if deal["version"] != expected_version:
        raise StaleVersionError(
            f"Version mismatch: expected {expected_version}, deal is at {deal['version']}"
        )

    deal["market_value"] = new_market_value
    deal["version"] += 1
    return dict(deal)


if __name__ == "__main__":
    user_a_view = dict(_DEALS["deal-1"])
    user_b_view = dict(_DEALS["deal-1"])

    result_a = update_deal("deal-1", user_a_view["version"], 13_000_000.0)
    print("User A update succeeded:", result_a)

    try:
        result_b = update_deal("deal-1", user_b_view["version"], 13_500_000.0)
        print("User B update succeeded:", result_b)
    except StaleVersionError as exc:
        print(f"User B update rejected: {exc}")