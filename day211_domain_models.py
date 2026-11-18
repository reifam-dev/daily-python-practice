"""Day 211 - Shared Domain Model with Pydantic.

One validated, immutable model that every later module can share,
instead of a new dict or class per file. Required fields stay required
(no silent `| None = None`), a validator must RETURN the cleaned value,
models are frozen so a bad value cannot be assigned after validation,
the collection inside is a tuple (a frozen model holding a list could
still be mutated), and money is Decimal - PCPP1 standard.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, computed_field, field_validator

Sector = Literal["logistics", "retail", "office"]


class Lease(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenant: str = Field(min_length=1)
    sector: Sector
    annual_rent: Decimal = Field(gt=0)
    years_remaining: float = Field(ge=0)

    @field_validator("tenant")
    @classmethod
    def clean_tenant(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("tenant must not be blank")
        return cleaned

    @computed_field  # type: ignore[prop-decorator]
    @property
    def monthly_rent(self) -> Decimal:
        return (self.annual_rent / 12).quantize(Decimal("0.01"))


class Deal(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1)
    price: Decimal = Field(gt=0)
    leases: tuple[Lease, ...] = ()

    @computed_field  # type: ignore[prop-decorator]
    @property
    def total_rent(self) -> Decimal:
        return sum((lease.annual_rent for lease in self.leases), Decimal("0"))


if __name__ == "__main__":
    lease = Lease.model_validate(
        {
            "tenant": " Acme Logistics ",
            "sector": "logistics",
            "annual_rent": "250000",
            "years_remaining": 3,
        }
    )
    print(repr(lease.tenant), lease.monthly_rent)

    deal = Deal(name="Riverside Estate", price=Decimal("8000000"), leases=(lease,))
    print(deal.total_rent)

    try:
        Lease.model_validate({"tenant": "Beta Retail", "annual_rent": "180000", "years_remaining": 7})
    except ValidationError as exc:
        print(f"Rejected: {exc.errors()[0]['loc'][0]} is required")
    try:
        lease.annual_rent = Decimal("-5")
    except ValidationError as exc:
        print(f"Rejected: {exc.errors()[0]['msg']}")