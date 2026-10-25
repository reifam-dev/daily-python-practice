"""Day 189 - Debt Covenants: DSCR, ICR and LTV.

DSCR = NOI / (interest + principal), ICR = NOI / interest, and
LTV = loan / value. A covenant is breached only when the ratio is
strictly on the wrong side of its limit - sitting exactly AT the limit
is compliant - PCPP1 standard.
"""
from __future__ import annotations


def dscr(noi: float, interest: float, principal: float) -> float:
    """Debt service cover: NOI over total debt service."""
    debt_service = interest + principal
    if debt_service <= 0:
        raise ValueError("debt service must be positive")
    return noi / debt_service


def icr(noi: float, interest: float) -> float:
    """Interest cover: NOI over interest only."""
    if interest <= 0:
        raise ValueError("interest must be positive")
    return noi / interest


def ltv(loan: float, value: float) -> float:
    """Loan-to-value: the loan as a fraction of the asset value."""
    if value <= 0:
        raise ValueError("value must be positive")
    return loan / value


def is_below_minimum(actual: float, minimum: float) -> bool:
    """True only if actual is strictly below a minimum covenant."""
    return actual < minimum


def is_above_maximum(actual: float, maximum: float) -> bool:
    """True only if actual is strictly above a maximum covenant."""
    return actual > maximum


def check_covenants(
    noi: float,
    interest: float,
    principal: float,
    loan: float,
    value: float,
    min_dscr: float = 1.25,
    min_icr: float = 2.0,
    max_ltv: float = 0.70,
) -> list[str]:
    """Return a human-readable line for every breached covenant."""
    breaches: list[str] = []
    actual_dscr = dscr(noi, interest, principal)
    actual_icr = icr(noi, interest)
    actual_ltv = ltv(loan, value)

    if is_below_minimum(actual_dscr, min_dscr):
        breaches.append(f"DSCR {actual_dscr:.2f} below minimum {min_dscr:.2f}")
    if is_below_minimum(actual_icr, min_icr):
        breaches.append(f"ICR {actual_icr:.2f} below minimum {min_icr:.2f}")
    if is_above_maximum(actual_ltv, max_ltv):
        breaches.append(f"LTV {actual_ltv:.1%} above maximum {max_ltv:.1%}")
    return breaches


if __name__ == "__main__":
    print(round(dscr(1_300_000.0, 600_000.0, 440_000.0), 4))
    print(round(ltv(12_000_000.0, 18_000_000.0), 4))
    print(is_below_minimum(1.25, 1.25))
    print(check_covenants(1_300_000.0, 600_000.0, 440_000.0, 12_000_000.0, 18_000_000.0))
    print(check_covenants(1_200_000.0, 600_000.0, 440_000.0, 12_000_000.0, 16_000_000.0))