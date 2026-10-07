"""Day 178 - NPV and IRR.

NPV discounts each flow by its period index (the day-0 outlay is not
discounted). IRR is found by bisection: NPV falls as the rate rises,
so a positive NPV means the true IRR is higher. The rate bracket is
validated first, so impossible inputs fail loudly - PCPP1 standard.
"""
from __future__ import annotations


def npv(rate: float, cash_flows: list[float]) -> float:
    """Net present value, with period 0 undiscounted."""
    return sum(cash_flow / (1 + rate) ** t for t, cash_flow in enumerate(cash_flows))


def irr(
    cash_flows: list[float],
    low: float = -0.99,
    high: float = 1.0,
    tolerance: float = 1e-9,
    max_iterations: int = 200,
) -> float:
    """Internal rate of return by bisection, or ValueError if not bracketed."""
    if npv(low, cash_flows) * npv(high, cash_flows) > 0:
        raise ValueError("IRR is not bracketed: NPV has the same sign at both ends")

    for _ in range(max_iterations):
        mid = (low + high) / 2
        value = npv(mid, cash_flows)
        if abs(value) < tolerance:
            return mid
        if value > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


if __name__ == "__main__":
    flows = [-1000.0, 300.0, 400.0, 500.0]
    print(round(npv(0.10, flows), 2))
    print(round(irr(flows), 4))
    try:
        irr([100.0, 100.0, 100.0])
    except ValueError as exc:
        print(f"Rejected: {exc}")