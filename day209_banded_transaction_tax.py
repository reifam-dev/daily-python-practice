"""Day 209 - Banded Transaction Tax (marginal bands, not a flat slab).

Each band's rate applies ONLY to the slice of the price that falls inside
that band: portion = max(0, min(price, upper) - lower). The last band is
open-ended. Illustrative bands below are the England and Northern Ireland
non-residential SDLT bands for 2026/27 (0% to 150,000, 2% to 250,000, 5%
above); Scotland and Wales differ, so the bands are a parameter and the
current official rates must always be checked. This is a coding exercise,
not tax advice - PCPP1 standard.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

Band = tuple[Decimal, Decimal, Decimal]

NON_RESIDENTIAL_BANDS: list[Band] = [
    (Decimal("0"), Decimal("150000"), Decimal("0")),
    (Decimal("150000"), Decimal("250000"), Decimal("0.02")),
    (Decimal("250000"), Decimal("Infinity"), Decimal("0.05")),
]


def banded_tax(price: Decimal, bands: list[Band] = NON_RESIDENTIAL_BANDS) -> Decimal:
    """Tax on price, charging each band's rate only on the slice inside it."""
    if price < 0:
        raise ValueError("price must not be negative")
    tax = Decimal("0")
    for lower, upper, rate in bands:
        portion = max(Decimal("0"), min(price, upper) - lower)
        tax += portion * rate
    return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def effective_rate(price: Decimal, bands: list[Band] = NON_RESIDENTIAL_BANDS) -> Decimal:
    """Tax as a share of price; zero for a zero price."""
    if price <= 0:
        return Decimal("0")
    return banded_tax(price, bands) / price


if __name__ == "__main__":
    for amount in ("100000", "1000000", "8000000"):
        price = Decimal(amount)
        print(f"{price:>10,}  tax {banded_tax(price):>10,}  effective {effective_rate(price):.2%}")
    print(effective_rate(Decimal("0")))