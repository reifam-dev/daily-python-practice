"""Day 210 - Money Value Object: Error Quiz. Find and fix three bugs."""


class Money:
    def __init__(self, amount, currency: str):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount

    def __repr__(self) -> str:
        return f"Money({self.amount!r}, {self.currency!r})"


if __name__ == "__main__":
    print(Money(0.1, "GBP") + Money(0.2, "GBP"))
    print(Money(10, "GBP") + Money(10, "EUR"))
    print(Money(10, "GBP") == Money(10, "EUR"))
    try:
        print(len({Money(10, "GBP"), Money(10, "GBP")}))
    except TypeError as exc:
        print(f"Crashed: {exc}")