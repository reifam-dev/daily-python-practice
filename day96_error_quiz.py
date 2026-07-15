"""Day 96 - pytest Advanced: Error Quiz.

Find and fix three bugs. No location hints.
"""
from dataclasses import dataclass

import pytest


@dataclass
class Deal:
    name: str
    market_value: float
    ltv: float


class ValuationError(Exception):
    """Raised when a deal fails valuation checks."""


def validate_ltv(deal: Deal, max_ltv: float = 0.65) -> None:
    if deal.ltv > max_ltv:
        raise ValuationError(f"{deal.name} exceeds max LTV of {max_ltv}")


def annualised_yield(net_income: float, market_value: float) -> float:
    return net_income / market_value


@pytest.fixture
def sample_deal():
    deal = Deal(name="Riverside JV", market_value=12_500_000.0, ltv=0.60)
    yield deal
    print(f"tearing down {deal.name}")


@pytest.fixture(scope="module")
def db_connection():
    connection = {"status": "open"}
    yield connection
    connection["status"] = "closed"


@pytest.mark.parametrize(
    "ltv,expected_error",
    [
        (0.50, False),
        (0.65, False),
        (0.70, True),
    ],
)
def test_validate_ltv(ltv, expected_error):
    deal = Deal(name="Test Deal", market_value=1_000_000.0, ltv=ltv)
    if expected_error:
        validate_ltv(deal)
    else:
        with pytest.raises(ValuationError):
            validate_ltv(deal)


def test_annualised_yield():
    result = annualised_yield(net_income=750_000.0, market_value=12_500_000.0)
    assert result == 0.06


def test_sample_deal_name(sample_deal):
    assert sample_deal.name = "Riverside JV"