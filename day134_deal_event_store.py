"""Day 134 - Event Sourcing: Deal Event Store.

Records every state change as an immutable event rather than
overwriting current state directly, and derives a deal's current
state on demand by replaying only that deal's events in order -
giving a full audit trail as a natural side effect - PCPP1 standard.
"""
from __future__ import annotations

_event_log: list[dict] = []


def record_event(deal_id: str, event_type: str, data: dict) -> None:
    """Append an immutable event to the log."""
    _event_log.append({"deal_id": deal_id, "event_type": event_type, "data": data})


def create_deal(deal_id: str, deal_name: str, market_value: float) -> None:
    record_event(deal_id, "created", {"deal_name": deal_name, "market_value": market_value})


def revalue_deal(deal_id: str, new_market_value: float) -> None:
    record_event(deal_id, "revalued", {"market_value": new_market_value})


def rebuild_deal_state(deal_id: str) -> dict:
    """Replay only this deal's events, in order, to derive its current state."""
    state: dict = {}
    for event in _event_log:
        if event["deal_id"] != deal_id:
            continue
        if event["event_type"] == "created":
            state["deal_name"] = event["data"]["deal_name"]
            state["market_value"] = event["data"]["market_value"]
        elif event["event_type"] == "revalued":
            state["market_value"] = event["data"]["market_value"]
    return state


def get_deal_history(deal_id: str) -> list[dict]:
    """Return the full, ordered event history for a single deal."""
    return [event for event in _event_log if event["deal_id"] == deal_id]


if __name__ == "__main__":
    create_deal("deal-1", "Riverside JV", 12_500_000.0)
    revalue_deal("deal-1", 13_000_000.0)
    create_deal("deal-2", "Westgate Retail", 8_100_000.0)
    revalue_deal("deal-1", 13_500_000.0)

    print("deal-1 state:", rebuild_deal_state("deal-1"))
    print("deal-2 state:", rebuild_deal_state("deal-2"))
    print("deal-1 history:", get_deal_history("deal-1"))