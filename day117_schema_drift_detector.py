"""Day 117 - Schema Drift Detection: Schema Drift Detector.

Scans an incoming batch of records against an expected schema,
flagging missing fields, wrong types, and unexpected extra fields
(a common sign of an upstream schema change) without crashing on
any single malformed record - PCPP1 standard.
"""
from __future__ import annotations

_EXPECTED_SCHEMA: dict[str, type] = {
    "deal_name": str,
    "market_value": float,
    "ltv": float,
}

_INCOMING_BATCH: list[dict] = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0, "ltv": 0.60},
    {"deal_name": "Westgate Retail", "market_value": 8_100_000.0},
    {"deal_name": "Logistics Portfolio", "market_value": "34200000", "ltv": 0.55},
    {"deal_name": "Docklands", "market_value": 15_750_000.0, "ltv": 0.55, "region": "Midlands"},
]


def check_schema(record: dict, schema: dict[str, type]) -> list[str]:
    """Compare a single record against the expected schema, returning any issues."""
    issues: list[str] = []

    for field, expected_type in schema.items():
        if field not in record:
            issues.append(f"missing field: {field}")
            continue
        if type(record[field]) is not expected_type:
            issues.append(
                f"wrong type for {field}: expected {expected_type.__name__}, "
                f"got {type(record[field]).__name__}"
            )

    extra_fields = set(record) - set(schema)
    for field in extra_fields:
        issues.append(f"unexpected field: {field}")

    return issues


def scan_batch(batch: list[dict], schema: dict[str, type]) -> dict[int, list[str]]:
    """Scan every record in a batch, returning issues keyed by record index."""
    report: dict[int, list[str]] = {}
    for i, record in enumerate(batch):
        issues = check_schema(record, schema)
        if issues:
            report[i] = issues
    return report


if __name__ == "__main__":
    report = scan_batch(_INCOMING_BATCH, _EXPECTED_SCHEMA)
    if not report:
        print("No schema drift detected.")
    for index, issues in report.items():
        print(f"Record {index}: {issues}")