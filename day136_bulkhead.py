"""Day 136 - Bulkhead Pattern: Deal Service Bulkheads.

Partitions concurrency capacity per downstream dependency, so a
saturated or slow "valuation service" bulkhead can't consume capacity
that a "pricing service" bulkhead needs, isolating failure the way a
ship's bulkheads contain flooding to one compartment - PCPP1
standard.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any


class BulkheadFullError(Exception):
    """Raised when a bulkhead has no available capacity."""


class Bulkhead:
    """Caps concurrent usage of one specific resource or dependency."""

    def __init__(self, name: str, max_concurrent: int) -> None:
        self.name = name
        self.max_concurrent = max_concurrent
        self.in_use = 0

    def acquire(self) -> bool:
        """Reserve one slot if capacity allows; return whether it succeeded."""
        if self.in_use < self.max_concurrent:
            self.in_use += 1
            return True
        return False

    def release(self) -> None:
        """Free one previously-acquired slot."""
        if self.in_use > 0:
            self.in_use -= 1


class BulkheadRegistry:
    """Holds a named bulkhead per dependency, isolating their capacity."""

    def __init__(self) -> None:
        self.bulkheads: dict[str, Bulkhead] = {}

    def register(self, name: str, max_concurrent: int) -> None:
        self.bulkheads[name] = Bulkhead(name, max_concurrent)

    def call_with_bulkhead(self, name: str, func: Callable[..., Any], *args: Any) -> Any:
        """Call func only if the named bulkhead has capacity, always releasing after."""
        bulkhead = self.bulkheads[name]
        if not bulkhead.acquire():
            raise BulkheadFullError(f"Bulkhead '{name}' is full")

        try:
            return func(*args)
        finally:
            bulkhead.release()


def slow_valuation_service(deal_name: str) -> str:
    return f"Valuation for {deal_name}"


if __name__ == "__main__":
    registry = BulkheadRegistry()
    registry.register("valuation_service", max_concurrent=2)
    registry.register("pricing_service", max_concurrent=2)

    registry.bulkheads["valuation_service"].acquire()
    registry.bulkheads["valuation_service"].acquire()

    try:
        result = registry.call_with_bulkhead(
            "valuation_service", slow_valuation_service, "Riverside JV"
        )
        print(result)
    except BulkheadFullError as exc:
        print(f"Rejected: {exc}")

    # a different bulkhead is entirely unaffected by valuation_service being full
    pricing_result = registry.call_with_bulkhead(
        "pricing_service", slow_valuation_service, "Westgate Retail"
    )
    print(pricing_result)