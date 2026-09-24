"""Day 167 - Strangler Fig Pattern: a facade routes each request to
either the legacy or modern system based on migration status, letting
functionality move over gradually rather than in one risky big-bang
cutover - PCPP1 standard."""
from __future__ import annotations


class LegacyDealSystem:
    def get_deal(self, deal_id: str) -> dict:
        return {"deal_id": deal_id, "market_value": 12_500_000.0, "source": "legacy"}


class ModernDealSystem:
    def __init__(self) -> None:
        self.migrated_deals: set[str] = {"deal-1"}

    def get_deal(self, deal_id: str) -> dict:
        return {"deal_id": deal_id, "market_value": 13_000_000.0, "source": "modern"}


class StranglerFacade:
    def __init__(self, legacy: LegacyDealSystem, modern: ModernDealSystem) -> None:
        self.legacy = legacy
        self.modern = modern

    def get_deal(self, deal_id: str) -> dict:
        if deal_id in self.modern.migrated_deals:
            return self.modern.get_deal(deal_id)
        return self.legacy.get_deal(deal_id)


if __name__ == "__main__":
    facade = StranglerFacade(LegacyDealSystem(), ModernDealSystem())
    print(facade.get_deal("deal-1"))  # source: modern
    print(facade.get_deal("deal-2"))  # source: legacy