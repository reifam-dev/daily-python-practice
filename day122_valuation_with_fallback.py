"""Day 122 - Graceful Degradation: Deal Valuation with Fallback.

Attempts a live valuation lookup, falling back to the last known good
cached value if the live service is unavailable, and only failing
outright if no cached value exists either - PCPP1 standard.
"""
from __future__ import annotations

_last_known_good: dict[str, float] = {}


class NoFallbackAvailableError(Exception):
    """Raised when a live call fails and no cached value exists either."""


def fetch_live_valuation(deal_name: str) -> float:
    """Simulate a live valuation lookup that may be unavailable."""
    if deal_name == "Riverside JV":
        raise ConnectionError("Valuation service unavailable")
    return 12_500_000.0


def get_valuation(deal_name: str) -> dict:
    """Fetch a live valuation and record it as the new last-known-good value."""
    value = fetch_live_valuation(deal_name)
    _last_known_good[deal_name] = value
    return {"deal_name": deal_name, "value": value, "source": "live"}


def get_valuation_with_fallback(deal_name: str) -> dict:
    """Fetch a live valuation, degrading gracefully to a cached value on failure."""
    try:
        return get_valuation(deal_name)
    except ConnectionError as exc:
        if deal_name not in _last_known_good:
            raise NoFallbackAvailableError(
                f"No cached value available for {deal_name}"
            ) from exc
        cached_value = _last_known_good[deal_name]
        return {"deal_name": deal_name, "value": cached_value, "source": "cached"}


if __name__ == "__main__":
    _last_known_good["Riverside JV"] = 12_000_000.0
    result = get_valuation_with_fallback("Riverside JV")
    print(result)

    result2 = get_valuation_with_fallback("Westgate Retail")
    print(result2)