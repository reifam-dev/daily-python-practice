"""Day 139 - CQRS: Error Quiz.

Find and fix three bugs. No location hints.
"""
_write_store = {}
_read_model = {}


def create_deal(deal_id: str, deal_name: str, market_value: float) -> None:
    _write_store[deal_id] = {"deal_name": deal_name, "market_value": market_value}


def update_deal_value(deal_id: str, new_market_value: float) -> None:
    _write_store[deal_id]["market_value"] = new_market_value
    _read_model[deal_id]["deal_name"] = _write_store[deal_id]["deal_name"]


def get_deal_summary(deal_id: str) -> dict:
    return _read_model.get(deal_id)


def list_all_summaries() -> list[dict]:
    return list(_write_store.keys())


if __name__ == "__main__":
    create_deal("deal-1", "Riverside JV", 12_500_000.0)
    print("summary:", get_deal_summary("deal-1"))

    update_deal_value("deal-1", 13_000_000.0)
    print("summary after update:", get_deal_summary("deal-1"))

    print("all summaries:", list_all_summaries())