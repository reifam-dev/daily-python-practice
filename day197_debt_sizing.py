"""Day 197 - Debt Sizing: the largest loan three lenders' tests allow.

A lender sizes the loan three ways and lends the LOWEST: (1) LTV caps
the loan at a share of value; (2) ICR caps interest at NOI / min ICR,
so loan = that interest / rate; (3) DSCR caps total debt service
(interest AND principal) at NOI / min DSCR, so loan = that service /
the amortising payment constant. The tightest test is the binding
constraint - PCPP1 standard.
"""
from __future__ import annotations


def payment_constant(annual_rate: float, years: int) -> float:
    """Annual debt service per 1 of loan for a level monthly-pay amortising loan."""
    if annual_rate == 0.0:
        return 1 / years
    monthly_rate = annual_rate / 12
    n = years * 12
    return 12 * monthly_rate / (1 - (1 + monthly_rate) ** -n)


def max_loan(
    noi: float,
    value: float,
    rate: float,
    amort_years: int,
    max_ltv: float = 0.65,
    min_icr: float = 2.0,
    min_dscr: float = 1.25,
) -> dict[str, float | str]:
    """Return the maximum loan, which test binds, and each test's own limit."""
    if noi <= 0 or value <= 0 or rate <= 0 or amort_years <= 0:
        raise ValueError("noi, value, rate and amort_years must be positive")

    limits = {
        "ltv": max_ltv * value,
        "icr": noi / min_icr / rate,
        "dscr": noi / min_dscr / payment_constant(rate, amort_years),
    }
    binding = min(limits, key=limits.get)
    return {"max_loan": limits[binding], "binding": binding, **limits}


if __name__ == "__main__":
    result = max_loan(1_000_000.0, 18_000_000.0, 0.055, 25)
    print({key: round(value) if not isinstance(value, str) else value for key, value in result.items()})