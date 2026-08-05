"""Day 117 - Schema Drift Detection: Error Quiz.

Find and fix three bugs. No location hints.
"""
EXPECTED_SCHEMA = {
    "deal_name": str,
    "market_value": float,
    "ltv": float,
}

INCOMING_BATCH = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0, "ltv": 0.60},
    {"deal_name": "Westgate Retail", "market_value": 8_100_000.0},
    {"deal_name": "Logistics Portfolio", "market_value": "34200000", "ltv": 0.55},
    {"deal_name": "Docklands", "market_value": 15_750_000.0, "ltv": 0.55, "region": "Midlands"},
]


def check_schema(record: dict, schema: dict) -> list[str]:
    issues = []
    for field, expected_type in schema.items():
        if field not in record:
            issues.append(f"missing field: {field}")
        if type(record[field]) != expected_type:
            issues.append(f"wrong type for {field}")
    return issues


def scan_batch(batch: list[dict], schema: dict) -> dict[int, list[str]]:
    report = {}
    for i, record in enumerate(batch):
        issues = check_schema(record, schema)
        report[i] = issues
    return report


if __name__ == "__main__":
    report = scan_batch(INCOMING_BATCH, EXPECTED_SCHEMA)
    for index, issues in report.items():
        print(index, issues)