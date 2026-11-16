"""Day 209 - Banded Transaction Tax: Error Quiz. Find and fix three bugs."""
from decimal import Decimal

BANDS = [
    (Decimal("0"), Decimal("150000"), Decimal("0")),
    (Decimal("150000"), Decimal("250000"), Decimal("0.02")),
    (Decimal("250000"), Decimal("1000000"), Decimal("0.05")),
]


def banded_tax(price: Decimal) -> Decimal:
    tax = Decimal("0")
    for lower, upper, rate in BANDS:
        portion = min(price, upper) - lower
        tax += portion * rate
    return tax


def effective_rate(price: Decimal) -> Decimal:
    return banded_tax(price) / price


if __name__ == "__main__":
    print(banded_tax(Decimal("100000")))
    print(banded_tax(Decimal("1000000")))
    print(banded_tax(Decimal("8000000")))
    print(effective_rate(Decimal("0")))