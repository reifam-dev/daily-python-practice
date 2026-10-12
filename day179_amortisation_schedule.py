"""Day 179 - Loan Amortisation Schedule.

Interest each month is charged on the outstanding balance at the
MONTHLY rate, the schedule covers every payment, a zero-rate loan is
handled as straight-line repayment, and the final balance is clamped
so float noise never shows as -0.00 - PCPP1 standard.
"""
from __future__ import annotations


def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """Level monthly payment for a fully amortising loan."""
    n = years * 12
    if annual_rate == 0.0:
        return principal / n
    monthly_rate = annual_rate / 12
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -n)


def build_schedule(
    principal: float, annual_rate: float, years: int
) -> list[tuple[int, float, float, float]]:
    """Return (month, interest, principal_paid, closing_balance) for every month."""
    n = years * 12
    monthly_rate = annual_rate / 12
    payment = monthly_payment(principal, annual_rate, years)
    balance = principal
    rows: list[tuple[int, float, float, float]] = []
    for month in range(1, n + 1):
        interest = balance * monthly_rate
        principal_paid = payment - interest
        balance = max(balance - principal_paid, 0.0)
        rows.append((month, round(interest, 2), round(principal_paid, 2), round(balance, 2)))
    return rows


if __name__ == "__main__":
    schedule = build_schedule(250_000.0, 0.05, 25)
    print(schedule[0])
    print(schedule[-1])
    print(len(schedule))
    print(len(build_schedule(120_000.0, 0.0, 10)))