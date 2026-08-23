"""Day 134 - Event Sourcing: Error Quiz.

Find and fix three bugs. No location hints.
"""
_event_log = []


def record_event(deal_id: str, event_type: str, data: dict) -> None:
    _event_log.append({"deal_id": deal_id, "event_type": event_type, "data": data})


def create_deal(deal_id: str, deal_name: str, market_value: float) -> None:
    record_event(deal_id, "created", {"deal_name": deal_name, "market_value": market_value})


def revalue_deal(deal_id: str, new_market_value: float) -> None:
    record_event(deal_id, "revalued", {"market_value": new_market_value})


def rebuild_deal_state(deal_id: str) -> dict:
    state = {}
    for event in _event_log:
        if event["event_type"] == "created":
            state["deal_name"] = event["data"]["deal_name"]
            state["market_value"] = event["data"]["market_value"]
        elif event["event_type"] == "revalued":
            state["market_value"] = event["data"]["market_value"]
    return state


if __name__ == "__main__":
    create_deal("deal-1", "Riverside JV", 12_500_000.0)
    revalue_deal("deal-1", 13_000_000.0)
    create_deal("deal-2", "Westgate Retail", 8_100_000.0)
    revalue_deal("deal-1", 13_500_000.0)

    print("deal-1 state:", rebuild_deal_state("deal-1"))
    print("deal-2 state:", rebuild_deal_state("deal-2"))