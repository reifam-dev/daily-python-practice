"""Day 116 - Deduplication: Error Quiz.

Find and fix three bugs. No location hints.
"""
RAW_RECORDS = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0, "source": "system_a"},
    {"deal_name": "riverside jv", "market_value": 12_500_000.0, "source": "system_b"},
    {"deal_name": "Westgate Retail", "market_value": 8_100_000.0, "source": "system_a"},
    {"deal_name": "Westgate Retail ", "market_value": 8_100_000.0, "source": "system_b"},
    {"deal_name": "Logistics Portfolio", "market_value": 34_200_000.0, "source": "system_a"},
]


def normalise_key(deal_name: str) -> str:
    return deal_name.lower()


def deduplicate(records: list[dict]) -> list[dict]:
    seen_keys = []
    deduplicated = []
    for record in records:
        key = normalise_key(record["deal_name"])
        if key in seen_keys:
            continue
        deduplicated.append(record)
    return deduplicated


if __name__ == "__main__":
    result = deduplicate(RAW_RECORDS)
    print(f"Original: {len(RAW_RECORDS)}, Deduplicated: {len(result)}")
    for record in result:
        print(record)