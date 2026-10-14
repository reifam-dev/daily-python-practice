"""Day 181 - Specification Pattern: composable deal-screening rules.

Each rule is a small object answering is_satisfied_by(deal). Rules
combine with AND / OR / NOT into new rules, so a screening policy is
built from reusable pieces instead of one tangled if-statement -
PCPP1 standard.
"""
from __future__ import annotations


class Specification:
    def is_satisfied_by(self, deal: dict) -> bool:
        raise NotImplementedError

    def and_(self, other: Specification) -> Specification:
        return AndSpecification(self, other)

    def or_(self, other: Specification) -> Specification:
        return OrSpecification(self, other)

    def not_(self) -> Specification:
        return NotSpecification(self)


class MinYieldSpec(Specification):
    def __init__(self, min_yield: float) -> None:
        self.min_yield = min_yield

    def is_satisfied_by(self, deal: dict) -> bool:
        return deal["yield"] >= self.min_yield


class MaxLtvSpec(Specification):
    def __init__(self, max_ltv: float) -> None:
        self.max_ltv = max_ltv

    def is_satisfied_by(self, deal: dict) -> bool:
        return deal["ltv"] <= self.max_ltv


class SectorSpec(Specification):
    def __init__(self, sector: str) -> None:
        self.sector = sector

    def is_satisfied_by(self, deal: dict) -> bool:
        return deal["sector"] == self.sector


class AndSpecification(Specification):
    def __init__(self, left: Specification, right: Specification) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, deal: dict) -> bool:
        return self.left.is_satisfied_by(deal) and self.right.is_satisfied_by(deal)


class OrSpecification(Specification):
    def __init__(self, left: Specification, right: Specification) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, deal: dict) -> bool:
        return self.left.is_satisfied_by(deal) or self.right.is_satisfied_by(deal)


class NotSpecification(Specification):
    def __init__(self, inner: Specification) -> None:
        self.inner = inner

    def is_satisfied_by(self, deal: dict) -> bool:
        return not self.inner.is_satisfied_by(deal)


if __name__ == "__main__":
    deals = [
        {"name": "Riverside JV", "yield": 0.062, "ltv": 0.60, "sector": "logistics"},
        {"name": "Westgate Retail", "yield": 0.071, "ltv": 0.70, "sector": "retail"},
        {"name": "Docklands", "yield": 0.055, "ltv": 0.55, "sector": "logistics"},
    ]
    screen = MinYieldSpec(0.06).and_(MaxLtvSpec(0.65)).and_(SectorSpec("retail").not_())
    print([d["name"] for d in deals if screen.is_satisfied_by(d)])