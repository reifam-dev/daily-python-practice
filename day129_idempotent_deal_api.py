"""Day 129 - API Idempotency Keys: Idempotent Deal Creation API.

Uses a client-supplied idempotency key to detect and safely handle a
duplicate request (e.g. a network-timeout retry), returning the
original response rather than creating a second deal - PCPP1
standard.
"""
from __future__ import annotations

_processed_requests: dict[str, dict] = {}


class IdempotencyKeyConflictError(Exception):
    """Raised when the same key is reused with genuinely different request data."""


def create_deal(idempotency_key: str, deal_name: str, market_value: float) -> dict:
    """Create a deal, or return the original result if this key was seen before."""
    if idempotency_key in _processed_requests:
        cached = _processed_requests[idempotency_key]
        if cached["deal_name"] != deal_name or cached["market_value"] != market_value:
            raise IdempotencyKeyConflictError(
                f"Key {idempotency_key} was already used with different request data"
            )
        return cached

    deal_id = len(_processed_requests) + 1
    result = {"id": deal_id, "deal_name": deal_name, "market_value": market_value}
    _processed_requests[idempotency_key] = result
    return result


if __name__ == "__main__":
    response1 = create_deal("key-abc-123", "Riverside JV", 12_500_000.0)
    print(response1)

    response2 = create_deal("key-abc-123", "Riverside JV", 12_500_000.0)
    print(response2)
    assert response1 == response2, "same key must return the same result"

    response3 = create_deal("key-xyz-789", "Westgate Retail", 8_100_000.0)
    print(response3)

    print(f"Total deals created: {len(_processed_requests)}")