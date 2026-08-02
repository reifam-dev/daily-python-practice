"""Day 114 - Data Validation Pipeline: Deal Row Validator.

Validates raw deal records against a Pydantic schema (including
domain-specific range checks on LTV), separating valid rows from
rejected ones with their error reasons, before loading into a
DataFrame - PCPP1 standard.
"""
from __future__ import annotations

import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator

_RAW_ROWS: list[dict] = [
    {"deal_name": "Riverside JV", "market_value": 12_500_000.0, "ltv": 0.60},
    {"deal_name": "", "market_value": 34_200_000.0, "ltv": 0.55},
    {"deal_name": "Westgate Retail", "market_value": -8_100_000.0, "ltv": 0.65},
    {"deal_name": "Docklands Logistics", "market_value": 15_750_000.0, "ltv": 1.20},
]


class DealRow(BaseModel):
    """Schema for a single validated deal row."""

    deal_name: str
    market_value: float
    ltv: float

    @field_validator("deal_name")
    @classmethod
    def deal_name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("deal_name cannot be empty")
        return value

    @field_validator("market_value")
    @classmethod
    def market_value_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("market_value must be positive")
        return value

    @field_validator("ltv")
    @classmethod
    def ltv_in_range(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError("ltv must be between 0.0 and 1.0")
        return value


def validate_rows(rows: list[dict]) -> tuple[list[DealRow], list[dict]]:
    """Split raw rows into valid DealRow instances and rejected rows with errors."""
    valid_rows: list[DealRow] = []
    errors: list[dict] = []
    for row in rows:
        try:
            valid_rows.append(DealRow(**row))
        except ValidationError as exc:
            errors.append({"row": row, "reason": str(exc)})
    return valid_rows, errors


def build_dataframe(rows: list[DealRow]) -> pd.DataFrame:
    """Convert validated DealRow instances into a DataFrame."""
    return pd.DataFrame([row.model_dump() for row in rows])


if __name__ == "__main__":
    valid, errors = validate_rows(_RAW_ROWS)
    print(f"Valid: {len(valid)}, Errors: {len(errors)}")
    for error in errors:
        print(f"  Rejected: {error['row']}")
    df = build_dataframe(valid)
    print(df)