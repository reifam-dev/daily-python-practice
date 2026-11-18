"""Day 210 - Money Value Object: an amount that knows its currency.

A bare float or Decimal cannot tell GBP from EUR and cannot stop 0.1 +
0.2 drifting. Money fixes this: the amount is a Decimal built from a
string (a float is refused), it is rounded to the penny on creation,
adding or comparing two currencies raises instead of silently mixing
them, and being a frozen dataclass it is immutable, compares by value
(amount AND currency) and is hashable - PCPP1 standard.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

_PENNY = Decimal("0.01")


class CurrencyMismatchError(Exception):
    """Raised when two Money values of different currencies are combined."""


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if isinstance(self.amount, float):
            raise TypeError("build Money from a string or Decimal, never a float")
        if len(self.currency) != 3 or not self.currency.isupper():
            raise ValueError("currency must be a 3-letter upper-case code")
        rounded = Decimal(self.amount).quantize(_PENNY, rounding=ROUND_HALF_UP)
        object.__setattr__(self, "amount", rounded)

    @classmethod
    def of(cls, amount: str, currency: str) -> Money:
        return cls(Decimal(amount), currency)

    def _require_same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(f"cannot combine {self.currency} and {other.currency}")

    def __add__(self, other: Money) -> Money:
        self._require_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        self._require_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: Decimal | int) -> Money:
        if isinstance(factor, float):
            raise TypeError("multiply by a Decimal or int, never a float")
        return Money(self.amount * Decimal(factor), self.currency)

    def __lt__(self, other: Money) -> bool:
        self._require_same_currency(other)
        return self.amount < other.amount

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:,.2f}"


if __name__ == "__main__":
    print(Money.of("0.10", "GBP") + Money.of("0.20", "GBP"))
    print(Money.of("1000000", "GBP") * Decimal("0.068"))
    print(Money.of("10", "GBP") == Money.of("10", "EUR"))
    print(len({Money.of("10", "GBP"), Money.of("10.00", "GBP")}))
    for attempt in (lambda: Money(0.1, "GBP"), lambda: Money.of("10", "GBP") + Money.of("10", "EUR")):
        try:
            attempt()
        except (TypeError, CurrencyMismatchError) as exc:
            print(f"Rejected: {exc}")