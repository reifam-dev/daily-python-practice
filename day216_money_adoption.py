"""Day 216 - Adopting the Money Type Across the Toolkit.

Days 177-214 left floats and Decimals mixed together. Adopting Money is
not a search and replace: it is a decision about boundaries. Floats
arriving from JSON or a CSV are converted ONCE, at the edge, with
Decimal(str(value)) - never Decimal(value), which preserves the binary
error it was meant to remove. Inside, amounts are Money and ratios stay
plain Decimal, because a yield is not a sum of money: Money times a
ratio is Money, and Money divided by Money is a ratio. Summing needs a
zero Money seed, since the built-in sum() starts at the integer 0 and a
Money refuses to be added to it - PCPP1 standard.
"""
from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal

from day210_money_value_object import Money

GBP = "GBP"


def to_money(value: str | int | Decimal | float, currency: str = GBP) -> Money:
    """Convert a value arriving from outside into Money, once, at the boundary."""
    if isinstance(value, float):
        return Money(Decimal(str(value)), currency)
    return Money(Decimal(value), currency)


def to_ratio(value: str | int | Decimal | float) -> Decimal:
    """A ratio is not money: it keeps no currency and is never rounded to the penny."""
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(value)


def apply_ratio(amount: Money, ratio: Decimal) -> Money:
    """Money times a ratio is Money; the ratio must not be a float."""
    if isinstance(ratio, float):
        raise TypeError("pass the ratio through to_ratio() before applying it")
    return amount * ratio


def divide(numerator: Money, denominator: Money) -> Decimal:
    """Money over Money is a dimensionless ratio, so it leaves the Money type behind."""
    if numerator.currency != denominator.currency:
        raise ValueError(f"cannot divide {numerator.currency} by {denominator.currency}")
    if denominator.amount == 0:
        raise ValueError("cannot divide by a zero amount")
    return numerator.amount / denominator.amount


def total(amounts: Iterable[Money], currency: str = GBP) -> Money:
    """Sum of Money, seeded with a zero Money rather than the integer 0."""
    return sum(amounts, Money.of("0", currency))


def acquisition_cost(price: Money, purchaser_costs: Decimal) -> Money:
    """Price plus purchaser's costs, where the costs are a ratio of the price."""
    return price + apply_ratio(price, purchaser_costs)


def net_initial_yield(net_rent: Money, acquisition: Money) -> Decimal:
    """Yield is a ratio, reported to four places, not an amount."""
    return divide(net_rent, acquisition).quantize(Decimal("0.0001"))


if __name__ == "__main__":
    payload = {"price": 8000000.0, "purchaser_costs_pct": 0.068, "rents": [250000.0, 180000.0]}

    print(f"naive Decimal(float): {Decimal(payload['purchaser_costs_pct'])}")
    print(f"boundary conversion:  {to_ratio(payload['purchaser_costs_pct'])}")

    price = to_money(payload["price"])
    costs = to_ratio(payload["purchaser_costs_pct"])
    acquisition = acquisition_cost(price, costs)
    rent = total(to_money(amount) for amount in payload["rents"])

    print(f"price {price}, acquisition {acquisition}")
    print(f"passing rent {rent}")
    print(f"net initial yield {net_initial_yield(rent, acquisition):.2%}")

    for attempt in (
        lambda: apply_ratio(price, 0.068),
        lambda: sum([rent]),
        lambda: divide(rent, Money.of("0", GBP)),
    ):
        try:
            attempt()
        except (TypeError, ValueError) as exc:
            print(f"Rejected: {exc}")