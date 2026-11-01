"""Day 194 - pytest parametrize and fixtures: tests for the Day 180 waterfall.

One parametrized test replaces four near-identical ones. The fixture is
function-scoped, so every test receives FRESH deal terms and one test
mutating them can never leak into another. Floats are compared with
pytest.approx, and the expected-error test uses pytest.raises - PCPP1
standard. Requires day180_distribution_waterfall.py in the same folder.
"""
import pytest

from day180_distribution_waterfall import run_waterfall

CAPITAL = 10_000_000.0
PREF_DUE = 2_400_000.0


@pytest.fixture
def terms() -> dict:
    """Fresh deal terms for every test."""
    return {"capital": CAPITAL, "pref_due": PREF_DUE, "gp_promote_pct": 0.20}


@pytest.mark.parametrize(
    "cash, expected_lp, expected_gp",
    [
        (15_000_000.0, 14_480_000.0, 520_000.0),  # full waterfall, promote paid
        (11_000_000.0, 11_000_000.0, 0.0),  # pref only partly covered
        (5_000_000.0, 5_000_000.0, 0.0),  # capital not fully returned
        (0.0, 0.0, 0.0),  # nothing to distribute
    ],
)
def test_lp_and_gp_totals(terms, cash, expected_lp, expected_gp):
    result = run_waterfall(cash, **terms)
    assert result["lp_total"] == pytest.approx(expected_lp)
    assert result["gp_total"] == pytest.approx(expected_gp)
    assert result["lp_total"] + result["gp_total"] == pytest.approx(cash)


@pytest.mark.parametrize(
    "cash, promote_pct",
    [(-1.0, 0.20), (1_000_000.0, 1.5), (1_000_000.0, -0.1)],
)
def test_invalid_inputs_rejected(terms, cash, promote_pct):
    terms["gp_promote_pct"] = promote_pct
    with pytest.raises(ValueError):
        run_waterfall(cash, **terms)


def test_each_test_gets_fresh_terms(terms):
    """Proves the mutation in the test above did not leak into this one."""
    assert terms["gp_promote_pct"] == 0.20