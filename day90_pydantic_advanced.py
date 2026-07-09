"""
Day 90 – Pydantic advanced: field_validator, model_validator, model inheritance, settings.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: pip install pydantic
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Any


class DealBase(BaseModel):
    """Base Pydantic model for a real estate deal."""

    sector: str = Field(..., description="Property sector.")
    region: str = Field(..., description="Geographic region.")
    value: float = Field(..., gt=0, description="Deal value in £m.")
    yield_pct: float = Field(..., gt=0, description="Net initial yield as a percentage.")


class DealCreate(DealBase):
    """Deal creation model with field-level validation."""

    @field_validator("sector")
    @classmethod
    def validate_sector(cls, v: str) -> str:
        """Validate sector against allowed values.

        Args:
            v: Sector string to validate.

        Returns:
            Validated sector string.

        Raises:
            ValueError: If sector is not in the allowed set.
        """
        allowed = {"Office", "Retail", "Industrial"}
        if v not in allowed:
            raise ValueError(f"Sector must be one of {allowed}. Got '{v}'.")
        return v

    @field_validator("yield_pct")
    @classmethod
    def validate_yield(cls, v: float) -> float:
        """Validate yield is within realistic bounds.

        Args:
            v: Yield percentage to validate.

        Returns:
            Validated yield percentage.

        Raises:
            ValueError: If yield exceeds 20%.
        """
        if v > 20.0:
            raise ValueError(f"Yield must be below 20%. Got {v}.")
        return round(v, 4)


class DealWithCV(DealCreate):
    """Deal model with computed capital value via model_validator."""

    capital_value: float = 0.0

    @model_validator(mode="after")
    def compute_capital_value(self) -> "DealWithCV":
        """Compute capital value after all fields are validated.

        Returns:
            Self with capital_value populated.
        """
        self.capital_value = self.value / (self.yield_pct / 100)
        return self

    def net_initial_yield(self) -> float:
        """Recalculate NIY from stored value and capital value.

        Returns:
            Net initial yield as a percentage.
        """
        return (self.value / self.capital_value) * 100


class PortfolioSettings(BaseModel):
    """Immutable settings model for portfolio configuration."""

    max_deals: int = Field(default=50, gt=0, description="Maximum number of deals.")
    max_single_exposure: float = Field(
        default=0.25, gt=0, le=1.0,
        description="Maximum single-deal exposure as a fraction of total portfolio."
    )
    allowed_sectors: list[str] = Field(
        default_factory=list,
        description="List of permitted property sectors."
    )
    debug: bool = Field(default=False, description="Enable debug mode.")

    model_config = {"frozen": True}

    def exposure_limit(self, total_portfolio_value: float) -> float:
        """Calculate maximum single-deal value given portfolio size.

        Args:
            total_portfolio_value: Total portfolio value in £m.

        Returns:
            Maximum single-deal exposure in £m.
        """
        return total_portfolio_value * self.max_single_exposure


class DealSummary(BaseModel):
    """Summary statistics model for a portfolio of deals."""

    total_deals: int = Field(..., gt=0, description="Total number of deals.")
    total_value: float = Field(..., gt=0, description="Total portfolio value in £m.")
    mean_yield: float = Field(..., gt=0, description="Mean net initial yield.")
    mean_cv: float = Field(..., gt=0, description="Mean capital value in £m.")

    @model_validator(mode="after")
    def validate_summary(self) -> "DealSummary":
        """Validate cross-field consistency of summary statistics.

        Returns:
            Self if valid.

        Raises:
            ValueError: If mean_cv is inconsistent with total_value and total_deals.
        """
        expected_mean_cv = self.total_value / self.total_deals
        if abs(self.mean_cv - expected_mean_cv) > 0.01:
            raise ValueError(
                f"mean_cv {self.mean_cv} inconsistent with "
                f"total_value / total_deals = {expected_mean_cv:.4f}."
            )
        return self

    @classmethod
    def from_deals(cls, deals: list["DealWithCV"]) -> "DealSummary":
        """Construct a DealSummary from a list of DealWithCV instances.

        Args:
            deals: List of DealWithCV objects.

        Returns:
            Populated DealSummary instance.
        """
        n = len(deals)
        total_value = sum(d.value for d in deals)
        mean_yield = sum(d.yield_pct for d in deals) / n
        mean_cv = sum(d.capital_value for d in deals) / n
        return cls(
            total_deals=n,
            total_value=total_value,
            mean_yield=round(mean_yield, 4),
            mean_cv=round(mean_cv, 4),
        )


if __name__ == "__main__":
    deals_data = [
        {"sector": "Office",     "region": "London",     "value": 80.0, "yield_pct": 4.5},
        {"sector": "Retail",     "region": "Manchester", "value": 30.0, "yield_pct": 5.5},
        {"sector": "Industrial", "region": "Birmingham", "value": 60.0, "yield_pct": 5.0},
    ]

    deals: list[DealWithCV] = [DealWithCV(**d) for d in deals_data]

    print("=== Individual deals ===")
    for deal in deals:
        print(f"  {deal.sector} | £{deal.value}m | {deal.yield_pct}% | CV=£{deal.capital_value:.1f}m")

    print("\n=== Portfolio settings ===")
    settings = PortfolioSettings(
        max_deals=30,
        max_single_exposure=0.20,
        allowed_sectors=["Office", "Industrial"],
    )
    print(settings)
    print(f"  Exposure limit on £500m portfolio: £{settings.exposure_limit(500):.1f}m")

    print("\n=== Summary ===")
    summary = DealSummary.from_deals(deals)
    print(summary)

    print("\n=== Validation errors ===")
    from pydantic import ValidationError
    try:
        DealCreate(sector="Residential", region="London", value=50.0, yield_pct=4.0)
    except ValidationError as e:
        print(f"  Caught: {e.errors()[0]['msg']}")

    try:
        DealCreate(sector="Office", region="London", value=50.0, yield_pct=25.0)
    except ValidationError as e:
        print(f"  Caught: {e.errors()[0]['msg']}")

    try:
        settings.max_deals = 100
    except Exception as e:
        print(f"  Frozen model: {e}")