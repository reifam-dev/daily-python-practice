"""Day 177 - Money Arithmetic: Decimal, not float, for currency.

Decimals are built from strings (never from floats), results are
rounded explicitly with a stated rounding mode, and splitting an
amount allocates the leftover pennies so the shares always sum back
to the original - PCPP1 standard.
"""
from __future__ import annotations

from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

_CENT = Decimal("0.01")


def total_fees(fees: list[Decimal]) -> Decimal:
    """Sum fees exactly, with no binary floating-point drift."""
    total = Decimal("0")
    for fee in fees:
        total += fee
    return total


def apply_rate(amount: Decimal, rate: Decimal) -> Decimal:
    """Multiply and round to the penny, half-up (the usual commercial rule)."""
    return (amount * rate).quantize(_CENT, rounding=ROUND_HALF_UP)


def split_evenly(amount: Decimal, parts: int) -> list[Decimal]:
    """Split an amount into penny-accurate shares that sum exactly to it."""
    if parts <= 0:
        raise ValueError("parts must be positive")
    base = (amount / parts).quantize(_CENT, rounding=ROUND_DOWN)
    leftover_pennies = int((amount - base * parts) / _CENT)
    shares = [base] * parts
    for i in range(leftover_pennies):
        shares[i] += _CENT
    return shares


if __name__ == "__main__":
    print(total_fees([Decimal("0.10"), Decimal("0.20")]))
    print(apply_rate(Decimal("0.10"), Decimal("3")))
    shares = split_evenly(Decimal("100.00"), 3)
    print(shares, sum(shares))
    assert sum(shares) == Decimal("100.00")