"""Day 156 - Builder Pattern: constructs a complex object step by
step via chained calls. Every with_*() method must return self for
the chain to work, and build() validates required fields are set
before producing the final object - PCPP1 standard."""
from __future__ import annotations


class IncompleteBuilderError(Exception):
    pass


class DealBuilder:
    def __init__(self) -> None:
        self.deal_name: str | None = None
        self.market_value: float | None = None
        self.ltv: float | None = None

    def with_name(self, name: str) -> DealBuilder:
        self.deal_name = name
        return self

    def with_market_value(self, value: float) -> DealBuilder:
        self.market_value = value
        return self

    def with_ltv(self, ltv: float) -> DealBuilder:
        self.ltv = ltv
        return self

    def build(self) -> dict:
        if self.deal_name is None or self.market_value is None:
            raise IncompleteBuilderError("deal_name and market_value are required")
        return {"deal_name": self.deal_name, "market_value": self.market_value, "ltv": self.ltv}


if __name__ == "__main__":
    deal = (
        DealBuilder()
        .with_name("Riverside JV")
        .with_market_value(12_500_000.0)
        .with_ltv(0.60)
        .build()
    )
    print(deal)