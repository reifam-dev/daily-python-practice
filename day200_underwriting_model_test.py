"""Day 200 - tests for the lease-by-lease underwriting model.

Covers the pieces that make the model easy to get subtly wrong: a lease
in its void year earns nothing, the acquisition outflow includes
purchaser's costs, voids depress NOI, and a higher exit cap rate must
lower the IRR. Requires day200_underwriting_model.py, day178_npv_irr.py
and day187_cap_rate_valuation.py in the same folder.
"""
from dataclasses import replace

import pytest

from day200_underwriting_model import (
    Assumptions,
    Lease,
    build_cash_flows,
    net_operating_income,
    underwrite,
    year_income,
)

LEASES = [
    Lease("Acme Logistics", 250_000.0, 3, 270_000.0),
    Lease("Beta Retail", 180_000.0, 7, 190_000.0),
    Lease("Gamma Office", 120_000.0, 2, 130_000.0),
]


@pytest.fixture
def assumptions() -> Assumptions:
    return Assumptions(
        price=8_000_000.0,
        purchaser_costs_pct=0.068,
        hold_years=5,
        void_years=1,
        opex_pct=0.10,
        exit_cap_rate=0.06,
        selling_costs_pct=0.015,
        discount_rate=0.08,
    )


@pytest.mark.parametrize(
    "year, expected",
    [
        (2, (250_000.0, 250_000.0)),  # inside the term: passing rent
        (4, (0.0, 270_000.0)),  # void year: no income, rent still "potential"
        (5, (270_000.0, 270_000.0)),  # re-let at ERV
    ],
)
def test_year_income_through_a_lease_lifecycle(year, expected):
    assert year_income(LEASES[0], year, 1) == expected


def test_cash_flow_shape_and_acquisition_outflow(assumptions):
    flows = build_cash_flows(LEASES, assumptions)
    assert len(flows) == assumptions.hold_years + 1
    assert flows[0] == pytest.approx(-8_000_000.0 * 1.068)


def test_voids_depress_noi(assumptions):
    year_two = net_operating_income(LEASES, 2, assumptions)
    year_three = net_operating_income(LEASES, 3, assumptions)
    assert year_three < year_two


def test_irr_falls_as_exit_cap_rate_rises(assumptions):
    irrs = [
        underwrite(LEASES, replace(assumptions, exit_cap_rate=cap))["unlevered_irr"]
        for cap in (0.05, 0.06, 0.07)
    ]
    assert irrs[0] > irrs[1] > irrs[2]


def test_equity_multiple_matches_cash_flows(assumptions):
    flows = build_cash_flows(LEASES, assumptions)
    result = underwrite(LEASES, assumptions)
    assert result["equity_multiple"] == pytest.approx(sum(flows[1:]) / -flows[0])


def test_invalid_hold_period_rejected(assumptions):
    with pytest.raises(ValueError):
        build_cash_flows(LEASES, replace(assumptions, hold_years=0))