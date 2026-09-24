"""Day 167 - Strangler Fig Pattern: Error Quiz. Find and fix three bugs."""
class LegacyDealSystem:
    def get_deal(self, deal_id: str) -> dict:
        return {"deal_id": deal_id, "market_value": 12_500_000.0, "source": "legacy"}


class ModernDealSystem:
    def __init__(self):
        self.migrated_deals = {"deal-1"}

    def get_deal(self, deal_id: str) -> dict:
        return {"deal_id": deal_id, "market_value": 13_000_000.0, "source": "modern"}


class StranglerFacade:
    def __init__(self, legacy: LegacyDealSystem, modern: ModernDealSystem):
        self.legacy = legacy
        self.modern = modern

    def get_deal(self, deal_id: str) -> dict:
        return self.legacy.get_deal(deal_id)


if __name__ == "__main__":
    facade = StranglerFacade(LegacyDealSystem(), ModernDealSystem())
    print(facade.get_deal("deal-1"))
    print(facade.get_deal("deal-2"))