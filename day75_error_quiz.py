# This file contains 3 deliberate bugs. Find and fix them.
import pytest


class Valuation:

    def __init__(self, noi: float, cap_rate: float) -> None:
        self._noi = noi
        self._cap_rate = cap_rate

    def capital_value(self) -> float:
        return self._noi / self._cap_rate

    def reversionary_yield(self, erv: float) -> float:
        return erv / self.capital_value() * 100


def test_capital_value_basic():
    v = Valuation(100_000, 0.05)
    assert v.capital_value() = 2_000_000       # Bug 1: = should be ==


@pytest.mark.parametrize("noi,cap_rate,expected", [
    (100_000, 0.05, 2_000_000),
    (200_000, 0.04, 5_000_000),
    (50_000,  0.10,   500_000),
])
def test_capital_value_param(noi, cap_rate, expected):
    v = Valuation(noi, cap_rate)
    assert v.capital_value() == expected


@pytest.fixture
def sample_valuation():
    return Valuation(120_000, 0.06)


def test_reversionary_yield(sample_valuation):
    result = sample_valuation.reversionary_yield(130_000)
    assert round(result, 2) == 6.5


def test_zero_cap_rate():
    v = Valuation(100_000, 0.0)
    with pytest.raises(ValueError):            # Bug 2: should be ZeroDivisionError
        v.capital_value()


def test_negative_noi():
    v = Valuation(-50_000, 0.05)
    assert v.capital_value() == 1_000_000      # Bug 3: should be -1_000_000