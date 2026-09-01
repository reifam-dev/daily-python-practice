"""Day 143 - Idempotent Consumer Pattern: Error Quiz.

Find and fix three bugs. No location hints.
"""
_deal_ledger = {}
_processed_message_ids = []


def process_deal_message(message_id: str, deal_id: str, market_value: float) -> str:
    if message_id in _processed_message_ids:
        return "skipped_duplicate"

    current = _deal_ledger.get(deal_id, 0.0)
    _deal_ledger[deal_id] = current + market_value

    return "processed"


if __name__ == "__main__":
    messages = [
        ("msg-1", "deal-1", 5_000_000.0),
        ("msg-2", "deal-1", 3_000_000.0),
        ("msg-1", "deal-1", 5_000_000.0),
        ("msg-3", "deal-2", 2_000_000.0),
    ]

    for message_id, deal_id, value in messages:
        outcome = process_deal_message(message_id, deal_id, value)
        print(f"{message_id}: {outcome}")

    print("Ledger:", _deal_ledger)