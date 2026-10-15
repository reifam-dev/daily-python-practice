"""Day 182 - Template Method Pattern: a fixed algorithm, pluggable steps.

The base class owns the ORDER of the algorithm (header, body, footer)
in generate(). Subclasses customise the individual steps (hooks) but
never replace generate() itself. body() is a genuine abstract method,
so an incomplete subclass fails at construction, not deep in a call -
PCPP1 standard.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    def header(self) -> str:
        return "=== DEAL REPORT ==="

    @abstractmethod
    def body(self) -> str:
        """Subclasses must supply the report body."""

    def footer(self) -> str:
        return "=== END ==="

    def generate(self) -> str:
        """The template method. Subclasses override hooks, not this."""
        parts = [self.header(), self.body(), self.footer()]
        return "\n".join(parts)


class DealReport(ReportGenerator):
    def __init__(self, deals: list[tuple[str, float]]) -> None:
        self.deals = deals

    def body(self) -> str:
        return "\n".join(f"{name}: {value:,.0f}" for name, value in self.deals)


class QuickReport(ReportGenerator):
    def __init__(self, deals: list[tuple[str, float]]) -> None:
        self.deals = deals

    def header(self) -> str:
        return "--- QUICK ---"

    def body(self) -> str:
        return ", ".join(name for name, _ in self.deals)


class SummaryReport(ReportGenerator):
    """Deliberately incomplete: forgets to implement body()."""


if __name__ == "__main__":
    deals = [("Riverside JV", 12_500_000.0), ("Westgate Retail", 8_100_000.0)]
    print(DealReport(deals).generate())
    print(QuickReport(deals).generate())
    try:
        SummaryReport()
    except TypeError as exc:
        print(f"Rejected: {exc}")