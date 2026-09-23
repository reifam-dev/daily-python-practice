"""Day 165 - Visitor Pattern: separates an operation (risk reporting)
from the object structure it operates on (Deal, LoanFacility), with
each accept() dispatching to a type-specific visit method - so new
operations can be added without modifying the item classes -
PCPP1 standard."""
from __future__ import annotations
from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod
    def visit_deal(self, deal: Deal) -> None: ...

    @abstractmethod
    def visit_loan_facility(self, facility: LoanFacility) -> None: ...


class Deal:
    def __init__(self, market_value: float) -> None:
        self.market_value = market_value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_deal(self)


class LoanFacility:
    def __init__(self, principal: float, rate: float) -> None:
        self.principal = principal
        self.rate = rate

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_loan_facility(self)


class RiskReportVisitor(Visitor):
    def visit_deal(self, deal: Deal) -> None:
        print(f"Deal risk: market_value={deal.market_value}")

    def visit_loan_facility(self, facility: LoanFacility) -> None:
        print(f"Loan risk: principal={facility.principal}, rate={facility.rate:.2%}")


if __name__ == "__main__":
    items = [Deal(12_500_000.0), LoanFacility(8_000_000.0, 0.0525)]
    visitor = RiskReportVisitor()
    for item in items:
        item.accept(visitor)