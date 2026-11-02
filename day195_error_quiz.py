"""Day 195 - CSV Import with Row-Level Errors: Error Quiz. Find and fix three bugs."""
import csv
import io

RAW = """tenant,sector,annual_rent,lease_end_month
Acme Logistics,logistics,250000,48
Beta Retail,retail,abc,24
Gamma Office,office,180000,36
,office,90000,12
Delta Office,office,90000,
"""


def import_rent_roll(text: str) -> tuple:
    rows = []
    errors = []
    reader = csv.DictReader(io.StringIO(text))
    for index, row in enumerate(reader):
        try:
            rows.append(
                {
                    "tenant": row["tenant"],
                    "sector": row["sector"],
                    "annual_rent": float(row["annual_rent"]),
                    "lease_end_month": int(row["lease_end_month"]),
                }
            )
        except:
            errors.append(f"row {index}: bad row")
    return rows, errors


if __name__ == "__main__":
    rows, errors = import_rent_roll(RAW)
    print([row["tenant"] for row in rows])
    print(errors)