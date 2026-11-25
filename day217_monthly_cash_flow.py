"""Day 217 - Monthly Cash-Flow Model.

An annual model hides everything that happens inside a year: rent-free
periods, a lease starting in month 7, a completion part-way through a
quarter. Moving to monthly periods fixes that but introduces three traps.
A rent-free month pays nothing, so the count of free months is a boundary
and off by one is the usual error. A lease starting in month 7 pays for
the months FROM 7 onward, not from month 1. And an IRR derived from
monthly flows is a MONTHLY rate: it annualises by compounding,
(1 + r) ** 12 - 1, never by multiplying by 12 - at 1% a month that is the
difference between 12.00% and 12.68% - PCPP1 standard.
"""
from __future__ import annotations

from dataclasses import dataclass

from day178_npv_irr import irr


@dataclass(frozen=True)
class MonthlyLease:
    """A lease on a monthly footing: when it starts and how long it is free."""

    tenant: str
    monthly_rent: float
    start_month: int
    rent_free_months: int = 0

    def __post_init__(self) -> None:
        if self.start_month < 1:
            raise ValueError("start_month is 1-based, so it must be at least 1")
        if self.monthly_rent <= 0:
            raise ValueError("monthly_rent must be positive")
        if self.rent_free_months < 0:
            raise ValueError("rent_free_months cannot be negative")

    def rent_in(self, month: int) -> float:
        """Rent paid in a given 1-based month: nothing before the start or while free."""
        if month < self.start_month:
            return 0.0
        if month < self.start_month + self.rent_free_months:
            return 0.0
        return self.monthly_rent


def monthly_income(leases: list[MonthlyLease], months: int) -> list[float]:
    """Total rent for each month from 1 to months inclusive."""
    return [sum(lease.rent_in(month) for lease in leases) for month in range(1, months + 1)]


def annualise(monthly_rate: float) -> float:
    """A monthly rate compounds; multiplying by 12 understates it."""
    return (1.0 + monthly_rate) ** 12 - 1.0


def build_monthly_flows(
    price: float, leases: list[MonthlyLease], months: int, exit_value: float
) -> list[float]:
    """Period 0 is the purchase; months 1..n carry rent; the sale lands in the last month."""
    flows = [-price]
    flows.extend(monthly_income(leases, months))
    flows[-1] += exit_value
    return flows


def monthly_irr(flows: list[float]) -> float:
    """Monthly IRR, found with the Day 178 bisection solver."""
    return irr(flows, low=-0.9, high=1.0)


if __name__ == "__main__":
    leases = [
        MonthlyLease("Acme Logistics", 20_833.33, start_month=1),
        MonthlyLease("Beta Retail", 15_000.00, start_month=1, rent_free_months=3),
        MonthlyLease("Gamma Office", 10_000.00, start_month=7),
    ]

    income = monthly_income(leases, 12)
    print(f"months 1-3:   {[round(value) for value in income[:3]]}")
    print(f"months 4-6:   {[round(value) for value in income[3:6]]}")
    print(f"months 7-9:   {[round(value) for value in income[6:9]]}")
    print(f"year 1 total: {round(sum(income)):,}")

    flows = build_monthly_flows(8_544_000.0, leases, 60, 9_091_500.0)
    monthly = monthly_irr(flows)
    print(f"monthly IRR {monthly:.4%}")
    print(f"annualised (compounded) {annualise(monthly):.2%}")
    print(f"annualised (times 12, wrong) {monthly * 12:.2%}")

    try:
        MonthlyLease("Bad", 1_000.0, start_month=0)
    except ValueError as exc:
        print(f"Rejected: {exc}")