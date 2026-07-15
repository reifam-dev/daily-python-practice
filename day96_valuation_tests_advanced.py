"""Day 96 - pytest Advanced: Valuation Test Suite.

Demonstrates fixtures with teardown, module-scoped fixtures,
parametrize with expected-exception cases, and approximate
floating-point assertions - PCPP1 standard.
"""
from __future__ import annotations

from dataclasses import dataclass

import pytest


@dataclass
class Deal:
    """A single real estate deal under valuation."""

    name: str
    market_value: float
    ltv: float


class ValuationError(Exception):
    """Raised when a deal fails valuation checks."""


def validate_ltv(deal: Deal, max_ltv: float = 0.65) -> None:
    """Raise ValuationError if a deal's loan-to-value exceeds the cap."""
    if deal.ltv > max_ltv:
        raise ValuationError(f"{deal.name} exceeds max LTV of {max_ltv}")


def annualised_yield(net_income: float, market_value: float) -> float:
    """Return the simple annualised yield for a deal."""
    return net_income / market_value


@pytest.fixture
def sample_deal():
    """Provide a single sample deal, with teardown logging."""
    deal = Deal(name="Riverside JV", market_value=12_500_000.0, ltv=0.60)
    yield deal
    print(f"tearing down {deal.name}")


@pytest.fixture(scope="module")
def db_connection():
    """Provide a fake, module-scoped database connection."""
    connection = {"status": "open"}
    yield connection
    connection["status"] = "closed"


@pytest.mark.parametrize(
    "ltv,should_raise",
    [
        (0.50, False),
        (0.65, False),
        (0.70, True),
    ],
)
def test_validate_ltv(ltv: float, should_raise: bool) -> None:
    """LTV at or below the cap passes silently; above it raises."""
    deal = Deal(name="Test Deal", market_value=1_000_000.0, ltv=ltv)
    if should_raise:
        with pytest.raises(ValuationError):
            validate_ltv(deal)
    else:
        validate_ltv(deal)


def test_annualised_yield() -> None:
    """Yield calculation should match within floating-point tolerance."""
    result = annualised_yield(net_income=750_000.0, market_value=12_500_000.0)
    assert result == pytest.approx(0.06)


def test_sample_deal_name(sample_deal: Deal) -> None:
    """The sample_deal fixture should provide the expected deal name."""
    assert sample_deal.name == "Riverside JV"


def test_db_connection_status(db_connection: dict) -> None:
    """The module-scoped connection should start open."""
    assert db_connection["status"] == "open"