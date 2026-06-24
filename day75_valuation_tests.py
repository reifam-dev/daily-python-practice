"""
Day 75 – pytest: unit testing, fixtures, parametrize, exception testing.
PCPP1 standard: type hints, docstrings, PEP 8, British English.
Run with: pytest day75_valuation_tests.py -v
"""

import pytest


class Valuation:
    """Represents a direct capitalisation property valuation."""

    def __init__(self, noi: float, cap_rate: float) -> None:
        """Initialise the valuation.

        Args:
            noi:      Net operating income in £.
            cap_rate: Capitalisation rate as a decimal (e.g. 0.05 for 5%).

        Raises:
            ValueError: If cap_rate is zero or negative.
        """
        if cap_rate <= 0:
            raise ValueError("Capitalisation rate must be positive.")
        self._noi: float = noi
        self._cap_rate: float = cap_rate

    def capital_value(self) -> float:
        """Calculate capital value using direct capitalisation.

        Returns:
            Capital value in £.
        """
        return self._noi / self._cap_rate

    def reversionary_yield(self, erv: float) -> float:
        """Calculate the reversionary yield given an estimated rental value.

        Args:
            erv: Estimated rental value in £.

        Returns:
            Reversionary yield as a percentage.
        """
        return (erv / self.capital_value()) * 100

    def equivalent_yield(self, passing_rent: float, erv: float) -> float:
        """Approximate equivalent yield as weighted mean.

        Args:
            passing_rent: Current contracted rent in £.
            erv:          Estimated rental value in £.

        Returns:
            Approximate equivalent yield as a percentage.
        """
        return ((passing_rent + erv) / 2 / self.capital_value()) * 100


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def office_valuation() -> Valuation:
    """Fixture: office valuation at 5% yield on £100k NOI."""
    return Valuation(100_000, 0.05)


@pytest.fixture
def retail_valuation() -> Valuation:
    """Fixture: retail valuation at 6% yield on £120k NOI."""
    return Valuation(120_000, 0.06)


# ── Unit Tests ────────────────────────────────────────────────────────────────

def test_capital_value_office(office_valuation: Valuation) -> None:
    """Capital value of £100k NOI at 5% should be £2m."""
    assert office_valuation.capital_value() == 2_000_000


def test_capital_value_retail(retail_valuation: Valuation) -> None:
    """Capital value of £120k NOI at 6% should be £2m."""
    assert retail_valuation.capital_value() == 2_000_000


@pytest.mark.parametrize("noi,cap_rate,expected", [
    (100_000, 0.05, 2_000_000),
    (200_000, 0.04, 5_000_000),
    (50_000,  0.10,   500_000),
    (300_000, 0.06, 5_000_000),
])
def test_capital_value_parametrised(noi: float, cap_rate: float, expected: float) -> None:
    """Parametrised test for capital value across multiple scenarios."""
    v = Valuation(noi, cap_rate)
    assert v.capital_value() == expected


def test_reversionary_yield(retail_valuation: Valuation) -> None:
    """Reversionary yield should be 6.50% when ERV is £130k on a £2m asset."""
    assert round(retail_valuation.reversionary_yield(130_000), 2) == 6.50


def test_zero_cap_rate_raises() -> None:
    """Valuation should raise ValueError when cap_rate is zero."""
    with pytest.raises(ValueError, match="Capitalisation rate must be positive"):
        Valuation(100_000, 0.0)


def test_negative_cap_rate_raises() -> None:
    """Valuation should raise ValueError when cap_rate is negative."""
    with pytest.raises(ValueError):
        Valuation(100_000, -0.05)


def test_negative_noi(office_valuation: Valuation) -> None:
    """Negative NOI should produce a negative capital value."""
    v = Valuation(-50_000, 0.05)
    assert v.capital_value() == -1_000_000


def test_equivalent_yield(office_valuation: Valuation) -> None:
    """Equivalent yield approximation should return a positive float."""
    result = office_valuation.equivalent_yield(90_000, 110_000)
    assert isinstance(result, float)
    assert result > 0