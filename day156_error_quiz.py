"""Day 156 - Builder Pattern: Error Quiz. Find and fix three bugs."""
class DealBuilder:
    def __init__(self):
        self.deal_name = None
        self.market_value = None
        self.ltv = None

    def with_name(self, name: str):
        self.deal_name = name

    def with_market_value(self, value: float):
        self.market_value = value
        return self

    def with_ltv(self, ltv: float):
        self.ltv = ltv
        return self

    def build(self) -> dict:
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