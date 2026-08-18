"""Day 130 - Optimistic Locking: Error Quiz.

Find and fix three bugs. No location hints.
"""
_DEALS = {
    "deal-1": {"deal_name": "Riverside JV", "market_value": 12_500_000.0, "version": 1},
}


def update_deal(deal_id: str, expected_version: int, new_market_value: float) -> dict:
    deal = _DEALS[deal_id]

    if deal["version"] == expected_version:
        raise ValueError(
            f"Version mismatch: expected {expected_version}, deal is at {deal['version']}"
        )

    deal["market_value"] = new_market_value
    deal["version"] += 1
    return deal


if __name__ == "__main__":
    user_a_view = dict(_DEALS["deal-1"])
    user_b_view = dict(_DEALS["deal-1"])

    result_a = update_deal("deal-1", user_a_view["version"], 13_000_000.0)
    print("User A update succeeded:", result_a)

    result_b = update_deal("deal-1", user_b_view["version"], 13_500_000.0)
    print("User B update succeeded:", result_b)