"""Day 129 - API Idempotency Keys: Error Quiz.

Find and fix three bugs. No location hints.
"""
_processed_requests = {}


def create_deal(idempotency_key: str, deal_name: str, market_value: float) -> dict:
    if idempotency_key in _processed_requests:
        return _processed_requests[idempotency_key]

    deal_id = len(_processed_requests) + 1
    result = {"id": deal_id, "deal_name": deal_name, "market_value": market_value}
    return result


if __name__ == "__main__":
    response1 = create_deal("key-abc-123", "Riverside JV", 12_500_000.0)
    print(response1)

    response2 = create_deal("key-abc-123", "Riverside JV", 12_500_000.0)
    print(response2)

    response3 = create_deal("key-xyz-789", "Westgate Retail", 8_100_000.0)
    print(response3)

    print(f"Total deals created: {len(_processed_requests)}")