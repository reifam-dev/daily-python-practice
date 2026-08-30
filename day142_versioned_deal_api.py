"""Day 142 - API Versioning Strategies: Versioned Deal API.

Serves multiple API versions side by side via explicit per-version
handlers, warns callers using a deprecated version, and fails clearly
(rather than crashing with an unhelpful internal error) when an
unknown version is requested - PCPP1 standard.
"""
from __future__ import annotations


class UnsupportedVersionError(Exception):
    """Raised when a client requests an API version that doesn't exist."""


class VersionedDealApi:
    """Serves a resource across multiple explicit, coexisting API versions."""

    def __init__(self) -> None:
        self.deprecated_versions = {"v1"}
        self._supported_versions = {"v1", "v2"}

    def get_deal_v1(self, deal_id: str) -> dict:
        return {"id": deal_id, "value": 12_500_000.0}

    def get_deal_v2(self, deal_id: str) -> dict:
        return {"id": deal_id, "market_value": 12_500_000.0, "currency": "GBP"}

    def handle_request(self, deal_id: str, version: str) -> dict:
        """Route a request to the correct versioned handler, or fail clearly."""
        if version not in self._supported_versions:
            raise UnsupportedVersionError(f"API version '{version}' is not supported")

        if version in self.deprecated_versions:
            print(f"Warning: {version} is deprecated")

        handler_name = f"get_deal_{version}"
        handler = getattr(self, handler_name)
        return handler(deal_id)


if __name__ == "__main__":
    api = VersionedDealApi()

    print(api.handle_request("deal-1", "v1"))
    print(api.handle_request("deal-1", "v2"))

    try:
        print(api.handle_request("deal-1", "v3"))
    except UnsupportedVersionError as exc:
        print(f"Rejected: {exc}")