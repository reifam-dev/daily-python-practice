"""Day 143 - Idempotent Consumer Pattern: Idempotent Deal Message Consumer.

Message queues typically guarantee "at-least-once" delivery, meaning
the same message can genuinely arrive twice. This consumer tracks
which message ids it has already applied, so a redelivered duplicate
is safely skipped rather than double-counted into the ledger -
PCPP1 standard.
"""
from __future__ import annotations

_deal_ledger: dict[str, float] = {}
_processed_message_ids: set[str] = set()


def process_deal_message(message_id: str, deal_id: str, market_value: float) -> str:
    """Apply a deal message to the ledger exactly once, regardless of redelivery."""
    if message_id in _processed_message_ids:
        return "skipped_duplicate"

    current = _deal_ledger.get(deal_id, 0.0)
    _deal_ledger[deal_id] = current + market_value
    _processed_message_ids.add(message_id)

    return "processed"


if __name__ == "__main__":
    messages = [
        ("msg-1", "deal-1", 5_000_000.0),
        ("msg-2", "deal-1", 3_000_000.0),
        ("msg-1", "deal-1", 5_000_000.0),  # redelivered duplicate of msg-1
        ("msg-3", "deal-2", 2_000_000.0),
    ]

    for message_id, deal_id, value in messages:
        outcome = process_deal_message(message_id, deal_id, value)
        print(f"{message_id}: {outcome}")

    print("Ledger:", _deal_ledger)
    assert _deal_ledger["deal-1"] == 8_000_000.0, "duplicate must not be double-counted"