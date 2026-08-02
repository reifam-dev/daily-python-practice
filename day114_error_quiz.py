"""Day 114 - Data Validation Pipeline: Error Quiz.

Find and fix three bugs. No location hints.
"""
import pandas as pd
from pydantic import BaseModel, ValidationError

RAW_ROWS = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0, "ltv": 0.60},
    {"deal_name": "", "market_value": 34_200_000.0, "ltv": 0.55},
    {"deal_name": "Westgate Retail", "market_value": -8_100_000.0, "ltv": 0.65},
    {"deal_name": "Docklands Logistics", "market_value": 15_750_000.0, "ltv": 1.20},
]


class DealRow(BaseModel):
    deal_name: str
    market_value: float
    ltv: float


def validate_rows(rows: list[dict]) -> tuple[list[DealRow], list[dict]]:
    valid_rows = []
    errors = []
    for row in rows:
        validated = DealRow(row)
        valid_rows.append(validated)
    return valid_rows, errors


def build_dataframe(rows: list[DealRow]) -> pd.DataFrame:
    return pd.DataFrame(rows)


if __name__ == "__main__":
    valid, errors = validate_rows(RAW_ROWS)
    print(f"Valid: {len(valid)}, Errors: {len(errors)}")
    df = build_dataframe(valid)
    print(df)