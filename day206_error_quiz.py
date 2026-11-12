"""Day 206 - Levered Returns and Negative Leverage: Error Quiz. Find and fix three bugs."""
from day178_npv_irr import irr


def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    monthly_rate = annual_rate / 12
    n = years * 12
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -n)


def loan_balance(principal: float, annual_rate: float, years: int, months_paid: int) -> float:
    monthly_rate = annual_rate / 12
    growth = (1 + monthly_rate) ** months_paid
    payment = monthly_payment(principal, annual_rate, years)
    return principal * growth - payment * (growth - 1) / monthly_rate


def levered_cash_flows(unlevered: list, loan: float, annual_rate: float, amort_years: int) -> list:
    hold_years = len(unlevered) - 1
    annual_service = monthly_payment(loan, annual_rate, amort_years) * 12
    flows = list(unlevered)
    flows[0] -= loan
    for year in range(1, hold_years + 1):
        flows[year] -= annual_service
    return flows


def leverage_effect(unlevered_irr: float, debt_rate: float) -> str:
    return "positive" if unlevered_irr < debt_rate else "negative"


if __name__ == "__main__":
    unlevered = [-8_544_000.0, 495_000.0, 495_000.0, 374_000.0, 252_000.0, 9_091_500.0]
    flows = levered_cash_flows(unlevered, 4_500_000.0, 0.055, 25)
    print([round(flow) for flow in flows])
    print(round(irr(unlevered), 4), leverage_effect(irr(unlevered), 0.055))