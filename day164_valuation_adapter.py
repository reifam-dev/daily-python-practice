"""Day 164 - Adapter Pattern: wraps an incompatible legacy interface
(pence, synchronous) behind the interface modern callers expect
(pounds as a float), converting units correctly at the boundary -
PCPP1 standard."""
from __future__ import annotations
from abc import ABC, abstractmethod


class LegacyValuationSystem:
    """Pre-existing system, returns values in whole pence, can't be changed."""

    def get_value_in_pence(self, deal_id: str) -> int:
        return 1_250_000_000


class ModernValuationApi(ABC):
    """The interface all valuation sources should present to callers."""

    @abstractmethod
    def get_market_value(self, deal_id: str) -> float:
        ...


class LegacyValuationAdapter(ModernValuationApi):
    """Adapts LegacyValuationSystem's pence-based API to the modern pounds interface."""

    def __init__(self, legacy_system: LegacyValuationSystem) -> None:
        self.legacy_system = legacy_system

    def get_market_value(self, deal_id: str) -> float:
        pence = self.legacy_system.get_value_in_pence(deal_id)
        return pence / 100.0


def print_valuation(api: ModernValuationApi, deal_id: str) -> None:
    print(f"{deal_id}: £{api.get_market_value(deal_id):,.2f}")


if __name__ == "__main__":
    legacy = LegacyValuationSystem()
    adapter = LegacyValuationAdapter(legacy)
    print_valuation(adapter, "deal-1")  # £12,500,000.00