"""Day 216 - Adopting the Money Type: Error Quiz. Find and fix three bugs."""
from decimal import Decimal

from day210_money_value_object import Money

GBP = "GBP"


def to_ratio(value):
    return Decimal(value)


def to_money(value, currency=GBP):
    return Money(Decimal(str(value)), currency)


def total(amounts):
    return sum(amounts)


def net_initial_yield(net_rent, acquisition):
    return (net_rent.amount / acquisition.amount).quantize(Decimal("0.01"))


if __name__ == "__main__":
    payload = {"price": 8000000.0, "purchaser_costs_pct": 0.068, "rents": [250000.0, 180000.0]}

    print(f"costs ratio: {to_ratio(payload['purchaser_costs_pct'])}")

    price = to_money(payload["price"])
    acquisition = price + price * to_ratio("0.068")
    rent_values = [to_money(amount) for amount in payload["rents"]]
    print(f"net initial yield: {net_initial_yield(to_money(430000.0), acquisition)}")

    try:
        print(f"passing rent: {total(rent_values)}")
    except TypeError as exc:
        print(f"Crashed: {exc}")