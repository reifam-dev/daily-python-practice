"""Day 187 - Direct Capitalisation and Net Initial Yield.

Value = NOI / cap rate. The NET initial yield divides NOI by the total
cost of acquiring the asset: the price PLUS the purchaser's costs
(stamp duty, agent and legal fees; roughly 6.8% is a common UK
assumption). Working backwards from a target yield, the price must be
the total cost divided back down by (1 + costs) - PCPP1 standard.
"""
from __future__ import annotations

import math


def value_from_cap_rate(noi: float, cap_rate: float) -> float:
    """Direct capitalisation value of an income stream."""
    if cap_rate <= 0:
        raise ValueError("cap_rate must be positive")
    return noi / cap_rate


def net_initial_yield(noi: float, price: float, costs_pct: float) -> float:
    """NOI as a percentage of price plus purchaser's costs."""
    if price <= 0:
        raise ValueError("price must be positive")
    return noi / (price * (1 + costs_pct))


def purchase_price_for_yield(noi: float, target_niy: float, costs_pct: float) -> float:
    """The headline price that delivers target_niy after purchaser's costs."""
    if target_niy <= 0:
        raise ValueError("target_niy must be positive")
    return noi / (target_niy * (1 + costs_pct))


if __name__ == "__main__":
    print(round(value_from_cap_rate(1_000_000.0, 0.055)))
    print(round(net_initial_yield(1_000_000.0, 18_000_000.0, 0.068), 4))
    price = purchase_price_for_yield(1_000_000.0, 0.052, 0.068)
    print(round(price))
    assert math.isclose(net_initial_yield(1_000_000.0, price, 0.068), 0.052)
    try:
        value_from_cap_rate(1_000_000.0, 0.0)
    except ValueError as exc:
        print(f"Rejected: {exc}")