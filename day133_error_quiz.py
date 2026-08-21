"""Day 133 - Outbox Pattern: Error Quiz.

Find and fix three bugs. No location hints.
"""
_deals = {}
_outbox = []
_published_events = []


def create_deal(deal_name: str, market_value: float) -> str:
    deal_id = f"deal-{len(_deals) + 1}"
    _deals[deal_id] = {"deal_name": deal_name, "market_value": market_value}
    return deal_id


def create_deal_with_event(deal_name: str, market_value: float) -> str:
    deal_id = create_deal(deal_name, market_value)
    event = {"type": "deal_created", "deal_id": deal_id, "deal_name": deal_name}
    _outbox.append(event)
    return deal_id


def publish_outbox_events() -> int:
    published_count = 0
    for event in _outbox:
        _published_events.append(event)
        published_count += 1
    return published_count


if __name__ == "__main__":
    create_deal_with_event("Riverside JV", 12_500_000.0)
    create_deal_with_event("Westgate Retail", 8_100_000.0)

    print(f"Outbox size before publishing: {len(_outbox)}")
    published = publish_outbox_events()
    print(f"Published: {published}")
    print(f"Outbox size after publishing: {len(_outbox)}")