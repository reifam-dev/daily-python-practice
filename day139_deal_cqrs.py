"""Day 139 - CQRS: Deal Command and Query Separation.

Commands (create_deal, update_deal_value) write to the source-of-truth
write store and explicitly keep the separately-maintained read model
in sync. Queries (get_deal_summary, list_all_summaries) only ever
read from the read model, never touching the write store directly -
PCPP1 standard.
"""
from __future__ import annotations

_write_store: dict[str, dict] = {}
_read_model: dict[str, dict] = {}


def create_deal(deal_id: str, deal_name: str, market_value: float) -> None:
    """Command: create a deal, writing through to both the store and read model."""
    _write_store[deal_id] = {"deal_name": deal_name, "market_value": market_value}
    _read_model[deal_id] = {"deal_name": deal_name, "market_value": market_value}


def update_deal_value(deal_id: str, new_market_value: float) -> None:
    """Command: update a deal's value, keeping the read model synchronised."""
    _write_store[deal_id]["market_value"] = new_market_value
    _read_model[deal_id]["market_value"] = new_market_value


def get_deal_summary(deal_id: str) -> dict | None:
    """Query: read a single deal's summary from the read model only."""
    return _read_model.get(deal_id)


def list_all_summaries() -> list[dict]:
    """Query: list every deal summary from the read model only."""
    return list(_read_model.values())


if __name__ == "__main__":
    create_deal("deal-1", "Riverside JV", 12_500_000.0)
    print("summary:", get_deal_summary("deal-1"))

    update_deal_value("deal-1", 13_000_000.0)
    print("summary after update:", get_deal_summary("deal-1"))

    print("all summaries:", list_all_summaries())