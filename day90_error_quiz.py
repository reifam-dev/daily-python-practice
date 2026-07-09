# This file contains 3 deliberate bugs. Find and fix them.
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Any


class DealBase(BaseModel):
    sector: str
    region: str
    value: float = Field(..., gt=0)
    yield_pct: float = Field(..., gt=0)


class DealCreate(DealBase):

    @field_validator("sector")
    def validate_sector(cls, v: str) -> str:   # Bug 1: missing @classmethod decorator
        allowed = {"Office", "Retail", "Industrial"}
        if v not in allowed:
            raise ValueError(f"Sector must be one of {allowed}.")
        return v

    @field_validator("yield_pct")
    @classmethod
    def validate_yield(cls, v: float) -> float:
        if v > 20.0:
            raise ValueError("Yield must be below 20%.")
        return v


class DealWithCV(DealCreate):

    capital_value: float = 0.0

    @model_validator(mode="after")
    def compute_capital_value(self) -> "DealWithCV":
        self.capital_value = self.value + (self.yield_pct / 100)  # Bug 2: + should be / (CV = value / (yield_pct / 100))
        return self


class PortfolioSettings(BaseModel):
    max_deals: int = Field(default=50, gt=0)
    max_single_exposure: float = Field(default=0.25, gt=0, le=1.0)
    allowed_sectors: list[str] = Field(default_factory=list)
    debug: bool = False

    model_config = {"frozen": True}

    def exposure_limit(self, total_portfolio_value: float) -> float:
        return total_portfolio_value * self.max_single_exposure


class DealSummary(BaseModel):
    total_deals: int
    total_value: float
    mean_yield: float
    mean_cv: float

    @model_validator(mode="after")
    def validate_summary(self) -> "DealSummary":
        if self.mean_yield <= 0:
            raise ValueError("Mean yield must be positive.")
        if self.total_deals != len([]):         # Bug 3: nonsensical check — should be if self.total_deals <= 0
            raise ValueError("Total deals must be positive.")
        return self


if __name__ == "__main__":
    deal = DealWithCV(sector="Office", region="London", value=80.0, yield_pct=4.5)
    print(deal)
    print(f"Capital value: £{deal.capital_value:.2f}m")
    settings = PortfolioSettings(
        max_deals=30,
        allowed_sectors=["Office", "Industrial"],
    )
    print(settings)
    print(f"Exposure limit on £500m portfolio: £{settings.exposure_limit(500):.1f}m")