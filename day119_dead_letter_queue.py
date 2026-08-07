"""Day 119 - Dead Letter Queue: Deal Processor with Dead Letter Queue.

Retries processing a record up to a fixed number of attempts, and
routes it to a dead letter queue with a recorded failure reason if
every attempt fails - so bad records are captured for later review
rather than silently dropped or retried forever - PCPP1 standard.
"""
from __future__ import annotations

_MAX_ATTEMPTS = 3

_RECORDS: list[dict] = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0},
    {"deal_name": "Bad Record", "market_value": "not_a_number"},
    {"deal_name": "Logistics Portfolio", "market_value": 34_200_000.0},
]

_dead_letter_queue: list[dict] = []


def process_record(record: dict) -> float:
    """Process a single record, raising if the data is malformed."""
    return record["market_value"] * 1.0


def process_with_dlq(record: dict) -> None:
    """Retry processing up to _MAX_ATTEMPTS times, then route to the DLQ."""
    attempts = 0
    last_error: Exception | None = None

    while attempts < _MAX_ATTEMPTS:
        try:
            result = process_record(record)
            print(f"Processed: {record['deal_name']} -> {result}")
            return
        except TypeError as exc:
            attempts += 1
            last_error = exc

    _dead_letter_queue.append({"record": record, "reason": str(last_error)})


if __name__ == "__main__":
    for record in _RECORDS:
        process_with_dlq(record)

    print(f"Dead letter queue size: {len(_dead_letter_queue)}")
    for entry in _dead_letter_queue:
        print(f"  Rejected: {entry['record']} - {entry['reason']}")