"""Day 164 - Adapter Pattern: Error Quiz. Find and fix three bugs."""
class LegacyValuationSystem:
    def get_value_in_pence(self, deal_id: str) -> int:
        return 1_250_000_000


class ModernValuationApi:
    def get_market_value(self, deal_id: str) -> float:
        raise NotImplementedError


class LegacyValuationAdapter(ModernValuationApi):
    def __init__(self, legacy_system: LegacyValuationSystem):
        self.legacy_system = legacy_system

    def get_market_value(self, deal_id: str) -> float:
        pence = self.legacy_system.get_value_in_pence(deal_id)
        return pence


def print_valuation(api: ModernValuationApi, deal_id: str) -> None:
    print(f"{deal_id}: £{api.get_market_value(deal_id):,.2f}")


if __name__ == "__main__":
    legacy = LegacyValuationSystem()
    adapter = LegacyValuationAdapter(legacy)
    print_valuation(adapter, "deal-1")