"""Day 200 - Milestone: Lease-by-Lease Underwriting Model.

The first exercise that CHAINS earlier building blocks into one model:
leases -> year-by-year NOI (with voids and re-letting) -> acquisition
and exit cash flows -> unlevered IRR, NPV and equity multiple. It reuses
irr/npv from Day 178 and value_from_cap_rate from Day 187 rather than
re-implementing them.

Simplifications, stated openly: a lease that ends is void for void_years
(no income, but operating costs continue on the rent it WOULD earn), then
re-lets at its ERV; operating costs are a share of that potential rent;
exit value is the final year's NOI over the exit cap rate - PCPP1 standard.
"""
from __future__ import annotations

from dataclasses import dataclass

from day178_npv_irr import irr, npv
from day187_cap_rate_valuation import value_from_cap_rate


@dataclass(frozen=True)
class Lease:
    tenant: str
    annual_rent: float
    end_year: int
    erv: float  # estimated rental value if re-let


@dataclass(frozen=True)
class Assumptions:
    price: float
    purchaser_costs_pct: float
    hold_years: int
    void_years: int
    opex_pct: float
    exit_cap_rate: float
    selling_costs_pct: float
    discount_rate: float


def year_income(lease: Lease, year: int, void_years: int) -> tuple[float, float]:
    """Return (actual_income, potential_income) for one lease in one year."""
    if year <= lease.end_year:
        return lease.annual_rent, lease.annual_rent
    if year <= lease.end_year + void_years:
        return 0.0, lease.erv
    return lease.erv, lease.erv


def net_operating_income(leases: list[Lease], year: int, assumptions: Assumptions) -> float:
    """Income actually received, less operating costs on the potential rent."""
    actual = 0.0
    potential = 0.0
    for lease in leases:
        lease_actual, lease_potential = year_income(lease, year, assumptions.void_years)
        actual += lease_actual
        potential += lease_potential
    return actual - assumptions.opex_pct * potential


def build_cash_flows(leases: list[Lease], assumptions: Assumptions) -> list[float]:
    """Year 0 outflow, one NOI per year held, and net sale proceeds in the last year."""
    if assumptions.hold_years <= 0:
        raise ValueError("hold_years must be positive")

    outflow = -assumptions.price * (1 + assumptions.purchaser_costs_pct)
    noi_by_year = [
        net_operating_income(leases, year, assumptions)
        for year in range(1, assumptions.hold_years + 1)
    ]
    flows = [outflow, *noi_by_year]

    exit_value = value_from_cap_rate(noi_by_year[-1], assumptions.exit_cap_rate)
    flows[-1] += exit_value * (1 - assumptions.selling_costs_pct)
    return flows


def underwrite(leases: list[Lease], assumptions: Assumptions) -> dict[str, float]:
    """Headline returns for the whole holding period."""
    flows = build_cash_flows(leases, assumptions)
    total_cost = -flows[0]
    return {
        "year_one_noi": net_operating_income(leases, 1, assumptions),
        "unlevered_irr": irr(flows),
        "npv": npv(assumptions.discount_rate, flows),
        "equity_multiple": sum(flows[1:]) / total_cost,
    }


if __name__ == "__main__":
    leases = [
        Lease("Acme Logistics", 250_000.0, 3, 270_000.0),
        Lease("Beta Retail", 180_000.0, 7, 190_000.0),
        Lease("Gamma Office", 120_000.0, 2, 130_000.0),
    ]
    assumptions = Assumptions(
        price=8_000_000.0,
        purchaser_costs_pct=0.068,
        hold_years=5,
        void_years=1,
        opex_pct=0.10,
        exit_cap_rate=0.06,
        selling_costs_pct=0.015,
        discount_rate=0.08,
    )
    print([round(flow) for flow in build_cash_flows(leases, assumptions)])
    print({key: round(value, 4) for key, value in underwrite(leases, assumptions).items()})