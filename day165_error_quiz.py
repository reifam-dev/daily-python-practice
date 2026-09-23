"""Day 165 - Visitor Pattern: Error Quiz. Find and fix three bugs."""
class Deal:
    def __init__(self, market_value: float):
        self.market_value = market_value

    def accept(self, visitor):
        visitor.visit(self)


class LoanFacility:
    def __init__(self, principal: float, rate: float):
        self.principal = principal
        self.rate = rate

    def accept(self, visitor):
        visitor.visit(self)


class RiskReportVisitor:
    def visit(self, item):
        if isinstance(item, Deal):
            print(f"Deal risk: market_value={item.market_value}")


if __name__ == "__main__":
    items = [Deal(12_500_000.0), LoanFacility(8_000_000.0, 0.0525)]
    visitor = RiskReportVisitor()
    for item in items:
        item.accept(visitor)