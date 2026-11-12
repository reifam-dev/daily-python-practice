"""Day 205 - XIRR: IRR for cash flows that fall on real dates.

Plain IRR assumes equally spaced periods; real deals pay on actual dates.
Each flow is discounted by its fractional years from the EARLIEST date
(days / 365, true division - floor division would throw away the
fraction), the flows are sorted first so input order cannot change the
answer, and an unbracketed problem (no sign change) fails loudly -
PCPP1 standard.
"""
from __future__ import annotations

from datetime import date


def xnpv(rate: float, flows: list[tuple[date, float]]) -> float:
    """Net present value of dated flows, measured from the earliest date."""
    ordered = sorted(flows, key=lambda flow: flow[0])
    start = ordered[0][0]
    return sum(
        amount / (1 + rate) ** ((when - start).days / 365) for when, amount in ordered
    )


def xirr(
    flows: list[tuple[date, float]],
    low: float = -0.99,
    high: float = 10.0,
    tolerance: float = 1e-9,
    max_iterations: int = 300,
) -> float:
    """Annualised IRR of dated flows by bisection."""
    if len(flows) < 2:
        raise ValueError("need at least two cash flows")
    if xnpv(low, flows) * xnpv(high, flows) > 0:
        raise ValueError("XIRR is not bracketed: NPV has the same sign at both ends")

    for _ in range(max_iterations):
        mid = (low + high) / 2
        value = xnpv(mid, flows)
        if abs(value) < tolerance:
            return mid
        if value > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


if __name__ == "__main__":
    flows = [
        (date(2026, 1, 1), -1_000_000.0),
        (date(2026, 7, 1), 50_000.0),
        (date(2027, 1, 1), 50_000.0),
        (date(2028, 6, 30), 1_200_000.0),
    ]
    print(round(xirr(flows), 4))
    print(round(xirr(list(reversed(flows))), 4))
    try:
        xirr([(date(2026, 1, 1), 100.0), (date(2027, 1, 1), 100.0)])
    except ValueError as exc:
        print(f"Rejected: {exc}")