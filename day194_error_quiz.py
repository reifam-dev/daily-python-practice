"""Day 194 - pytest parametrize and fixtures: Error Quiz. Find and fix three bugs.

Read this as a pytest module (it would live in a file named *_test.py).
"""
import pytest

from day180_distribution_waterfall import run_waterfall


@pytest.fixture(scope="module")
def terms() -> dict:
    return {"capital": 10_000_000.0, "pref_due": 2_400_000.0, "gp_promote_pct": 0.20}


@pytest.mark.parametrize(
    "cash, expected_lp, expected_gp",
    [
        (15_000_000.0, 14_480_000.0, 520_000.0),
        (11_000_000.0, 11_000_000.0, 0.0),
        (5_000_000.0, 5_000_000.0),
    ],
)
def test_lp_and_gp_totals(terms, cash, expected_lp, expected_gp):
    result = run_waterfall(cash, **terms)
    assert result["lp_total"] == expected_lp
    assert result["gp_total"] == expected_gp


def test_invalid_promote_rejected(terms):
    terms["gp_promote_pct"] = 1.5
    with pytest.raises(ValueError):
        run_waterfall(1_000_000.0, **terms)


def test_totals_add_up(terms):
    result = run_waterfall(15_000_000.0, **terms)
    assert (result["lp_total"] + result["gp_total"] == 15_000_000.0, "totals must add up")