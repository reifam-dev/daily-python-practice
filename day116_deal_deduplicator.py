"""Day 116 - Deduplication: Deal Deduplicator.

Merges near-duplicate deal records that arrive with inconsistent
formatting (case, whitespace) from different source systems, keeping
the first-seen record for each normalised key - PCPP1 standard.
"""
from __future__ import annotations

_RAW_RECORDS: list[dict] = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0, "source": "system_a"},
    {"deal_name": "riverside jv", "market_value": 12_500_000.0, "source": "system_b"},
    {"deal_name": "Westgate Retail", "market_value": 8_100_000.0, "source": "system_a"},
    {"deal_name": "Westgate Retail ", "market_value": 8_100_000.0, "source": "system_b"},
    {"deal_name": "Logistics Portfolio", "market_value": 34_200_000.0, "source": "system_a"},
]


def normalise_key(deal_name: str) -> str:
    """Return a normalised key for matching near-duplicate deal names."""
    return deal_name.strip().lower()


def deduplicate(records: list[dict]) -> list[dict]:
    """Remove near-duplicate records, keeping the first occurrence of each key."""
    seen_keys: set[str] = set()
    deduplicated: list[dict] = []
    for record in records:
        key = normalise_key(record["deal_name"])
        if key in seen_keys:
            continue
        seen_keys.add(key)
        deduplicated.append(record)
    return deduplicated


if __name__ == "__main__":
    result = deduplicate(_RAW_RECORDS)
    print(f"Original: {len(_RAW_RECORDS)}, Deduplicated: {len(result)}")
    for record in result:
        print(record)