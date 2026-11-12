"""Day 205 - XIRR (dated cash flows): Error Quiz. Find and fix three bugs."""
from datetime import date


def xnpv(rate: float, flows: list) -> float:
    total = 0.0
    previous = flows[0][0]
    for when, amount in flows:
        years = (when - previous).days // 365
        total += amount / (1 + rate) ** years
        previous = when
    return total


def xirr(flows: list, low: float = -0.99, high: float = 10.0) -> float:
    for _ in range(200):
        mid = (low + high) / 2
        if xnpv(mid, flows) > 0:
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
    print(round(xirr([(date(2026, 1, 1), 100.0), (date(2027, 1, 1), 100.0)]), 4))