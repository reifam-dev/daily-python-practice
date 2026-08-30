"""Day 142 - API Versioning Strategies: Error Quiz.

Find and fix three bugs. No location hints.
"""
class VersionedDealApi:
    def __init__(self):
        self.deprecated_versions = {"v1"}

    def get_deal_v1(self, deal_id: str) -> dict:
        return {"id": deal_id, "value": 12_500_000.0}

    def get_deal_v2(self, deal_id: str) -> dict:
        return {"id": deal_id, "market_value": 12_500_000.0, "currency": "GBP"}

    def handle_request(self, deal_id: str, version: str) -> dict:
        if version in self.deprecated_versions:
            print(f"Warning: {version} is deprecated")

        handler_name = f"get_deal_{version}"
        handler = getattr(self, handler_name)
        return handler(deal_id)


if __name__ == "__main__":
    api = VersionedDealApi()

    print(api.handle_request("deal-1", "v1"))
    print(api.handle_request("deal-1", "v2"))
    print(api.handle_request("deal-1", "v3"))