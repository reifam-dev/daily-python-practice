"""Day 211 - Shared Domain Model with Pydantic: Error Quiz. Find and fix three bugs."""
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class Lease(BaseModel):
    tenant: str = Field(min_length=1)
    sector: str | None = None
    annual_rent: Decimal = Field(gt=0)
    years_remaining: float = Field(ge=0)

    @field_validator("tenant")
    @classmethod
    def clean_tenant(cls, value: str) -> str:
        value.strip()


if __name__ == "__main__":
    lease = Lease.model_validate(
        {"tenant": " Acme Logistics ", "annual_rent": "250000", "years_remaining": 3}
    )
    print(repr(lease.tenant))
    print(lease.sector)
    lease.annual_rent = Decimal("-5")
    print(lease.annual_rent)