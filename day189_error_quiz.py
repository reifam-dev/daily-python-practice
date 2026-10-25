"""Day 189 - Debt Covenants (DSCR, ICR, LTV): Error Quiz. Find and fix three bugs."""


def dscr(noi: float, interest: float, principal: float) -> float:
    return noi / interest


def ltv(loan: float, value: float) -> float:
    return value / loan


def is_breach(actual: float, minimum: float) -> bool:
    return actual <= minimum


if __name__ == "__main__":
    print(round(dscr(1_300_000.0, 600_000.0, 440_000.0), 4))
    print(round(ltv(12_000_000.0, 18_000_000.0), 4))
    print(is_breach(1.25, 1.25))