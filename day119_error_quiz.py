"""Day 119 - Dead Letter Queue: Error Quiz.

Find and fix three bugs. No location hints.
"""
MAX_ATTEMPTS = 3

RECORDS = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0},
    {"deal_name": "Bad Record", "market_value": "not_a_number"},
    {"deal_name": "Logistics Portfolio", "market_value": 34_200_000.0},
]

dead_letter_queue = []


def process_record(record: dict) -> float:
    return record["market_value"] * 1.0


def process_with_dlq(record: dict) -> None:
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            result = process_record(record)
            print(f"Processed: {record['deal_name']} -> {result}")
            return
        except TypeError:
            attempts += 1

    dead_letter_queue.append(record)


if __name__ == "__main__":
    for record in RECORDS:
        process_with_dlq(record)

    print(f"Dead letter queue size: {len(dead_letter_queue)}")