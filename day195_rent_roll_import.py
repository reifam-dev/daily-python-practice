"""Day 195 - CSV Import with Row-Level Errors.

A bad row is reported with its real FILE line number (reader.line_num,
which counts the header) and the actual reason, then skipped - one bad
row never aborts the whole import. Required fields are validated, and
only the expected exception types are caught - PCPP1 standard.
"""
from __future__ import annotations

import csv
import io

RAW = """tenant,sector,annual_rent,lease_end_month
Acme Logistics,logistics,250000,48
Beta Retail,retail,abc,24
Gamma Office,office,180000,36
,office,90000,12
Delta Office,office,90000,
"""


def import_rent_roll(text: str) -> tuple[list[dict], list[str]]:
    """Return (valid_rows, error_messages) for a rent roll in CSV form."""
    valid: list[dict] = []
    errors: list[str] = []
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        line = reader.line_num
        try:
            tenant = (row["tenant"] or "").strip()
            if not tenant:
                raise ValueError("tenant is blank")
            annual_rent = float(row["annual_rent"])
            if annual_rent <= 0:
                raise ValueError("annual_rent must be positive")
            lease_end_month = int(row["lease_end_month"])
        except (KeyError, ValueError) as exc:
            errors.append(f"line {line}: {exc}")
            continue
        valid.append(
            {
                "tenant": tenant,
                "sector": row["sector"],
                "annual_rent": annual_rent,
                "lease_end_month": lease_end_month,
            }
        )
    return valid, errors


if __name__ == "__main__":
    rows, errors = import_rent_roll(RAW)
    print([row["tenant"] for row in rows])
    for message in errors:
        print(message)