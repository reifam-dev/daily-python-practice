"""Day 133 - Outbox Pattern: Deal Creation Outbox.

Writes a deal and its corresponding "deal created" event atomically
(both succeed or both fail together, since they're just two writes to
the same in-memory store here - in a real system this would be one
database transaction), then publishes queued events separately,
removing each only once genuinely published - PCPP1 standard.
"""
from __future__ import annotations

_deals: dict[str, dict] = {}
_outbox: list[dict] = []
_published_events: list[dict] = []


def create_deal(deal_name: str, market_value: float) -> str:
    deal_id = f"deal-{len(_deals) + 1}"
    _deals[deal_id] = {"deal_name": deal_name, "market_value": market_value}
    return deal_id


def create_deal_with_event(deal_name: str, market_value: float) -> str:
    """Create a deal and queue its creation event in the same logical step."""
    deal_id = create_deal(deal_name, market_value)
    event = {"type": "deal_created", "deal_id": deal_id, "deal_name": deal_name}
    _outbox.append(event)
    return deal_id


def publish_outbox_events() -> int:
    """Publish every queued event, removing it from the outbox only once sent."""
    published_count = 0
    while _outbox:
        event = _outbox[0]
        _published_events.append(event)
        _outbox.pop(0)
        published_count += 1
    return published_count


if __name__ == "__main__":
    create_deal_with_event("Riverside JV", 12_500_000.0)
    create_deal_with_event("Westgate Retail", 8_100_000.0)

    print(f"Outbox size before publishing: {len(_outbox)}")
    published = publish_outbox_events()
    print(f"Published: {published}")
    print(f"Outbox size after publishing: {len(_outbox)}")