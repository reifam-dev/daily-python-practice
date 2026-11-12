"""Day 206 - Levered Returns and Negative Leverage.

Borrowing changes the equity cash flows in three places: the loan
REDUCES the day-0 equity cheque, every year pays debt service (interest
AND principal), and the outstanding balance is repaid out of the sale
proceeds. Leverage helps only when the asset's unlevered return
EXCEEDS the cost of debt - otherwise it is negative leverage and
the levered IRR falls below the unlevered one - PCPP1 standard.
"""
from __future__ import annotations

from day178_npv_irr import irr


def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """Level monthly payment for a fully amortising loan."""
    n = years * 12
    if annual_rate == 0.0:
        return principal / n
    monthly_rate = annual_rate / 12
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -n)


def loan_balance(principal: float, annual_rate: float, years: int, months_paid: int) -> float:
    """Outstanding balance after months_paid level payments."""
    if annual_rate == 0.0:
        return principal * (1 - months_paid / (years * 12))
    monthly_rate = annual_rate / 12
    growth = (1 + monthly_rate) ** months_paid
    payment = monthly_payment(principal, annual_rate, years)
    return principal * growth - payment * (growth - 1) / monthly_rate


def levered_cash_flows(
    unlevered: list[float], loan: float, annual_rate: float, amort_years: int
) -> list[float]:
    """Equity cash flows after the loan: proceeds in, debt service out, balance repaid."""
    hold_years = len(unlevered) - 1
    annual_service = monthly_payment(loan, annual_rate, amort_years) * 12

    flows = list(unlevered)
    flows[0] += loan
    for year in range(1, hold_years + 1):
        flows[year] -= annual_service
    flows[-1] -= loan_balance(loan, annual_rate, amort_years, hold_years * 12)
    return flows


def leverage_effect(unlevered_irr: float, debt_rate: float) -> str:
    """Positive only if the asset earns more than the debt costs."""
    if unlevered_irr > debt_rate:
        return "positive"
    if unlevered_irr < debt_rate:
        return "negative"
    return "neutral"


if __name__ == "__main__":
    unlevered = [-8_544_000.0, 495_000.0, 495_000.0, 374_000.0, 252_000.0, 9_091_500.0]
    flows = levered_cash_flows(unlevered, 4_500_000.0, 0.055, 25)
    print([round(flow) for flow in flows])
    print(f"unlevered {irr(unlevered):.2%}, levered {irr(flows):.2%}")
    print(leverage_effect(irr(unlevered), 0.055))