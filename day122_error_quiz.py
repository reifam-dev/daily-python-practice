"""Day 122 - Graceful Degradation: Error Quiz.

Find and fix three bugs. No location hints.
"""
_LAST_KNOWN_GOOD = {}


def fetch_live_valuation(deal_name: str) -> float:
    if deal_name == "Riverside JV":
        raise ConnectionError("Valuation service unavailable")
    return 12_500_000.0


def get_valuation(deal_name: str) -> dict:
    value = fetch_live_valuation(deal_name)
    _LAST_KNOWN_GOOD[deal_name] = value
    return {"deal_name": deal_name, "value": value, "source": "live"}


def get_valuation_with_fallback(deal_name: str) -> dict:
    try:
        return get_valuation(deal_name)
    except ConnectionError:
        cached_value = _LAST_KNOWN_GOOD[deal_name]
        return {"deal_name": deal_name, "value": cached_value, "source": "cached"}


if __name__ == "__main__":
    _LAST_KNOWN_GOOD["Riverside JV"] = 12_000_000.0
    result = get_valuation_with_fallback("Riverside JV")
    print(result)

    result2 = get_valuation_with_fallback("Westgate Retail")
    print(result2)