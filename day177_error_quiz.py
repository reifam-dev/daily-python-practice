"""Day 177 - Money Arithmetic: Error Quiz. Find and fix three bugs."""
from decimal import Decimal


def total_fees(fees: list) -> float:
    total = 0.0
    for fee in fees:
        total += fee
    return total


def apply_rate(amount: Decimal, rate: Decimal) -> Decimal:
    return amount * rate


def split_evenly(amount: Decimal, parts: int) -> list:
    share = round(amount / parts, 2)
    return [share] * parts


if __name__ == "__main__":
    print(total_fees([0.10, 0.20]))
    print(apply_rate(Decimal(0.1), Decimal("3")))
    shares = split_evenly(Decimal("100.00"), 3)
    print(shares, sum(shares))