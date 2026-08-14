"""Day 126 - Distributed Tracing with Correlation IDs: Correlated Deal Pipeline.

Generates a single correlation id per incoming request and threads it
through every log line produced while handling that request, so all
log output for one call can be filtered and reconstructed later, even
when interleaved with other concurrent requests - PCPP1 standard.
"""
from __future__ import annotations

import logging
import uuid

_logger = logging.getLogger("deal_pipeline")
_logger.setLevel(logging.INFO)
if not _logger.handlers:
    _logger.addHandler(logging.StreamHandler())


def start_request() -> str:
    """Generate a new correlation id as a string for a fresh request."""
    return str(uuid.uuid4())


def fetch_deal(deal_name: str, correlation_id: str) -> dict:
    """Fetch a deal, tagging the log line with the request's correlation id."""
    _logger.info(f"[{correlation_id}] Fetching deal: {deal_name}")
    return {"deal_name": deal_name, "market_value": 12_500_000.0}


def score_deal(deal: dict, correlation_id: str) -> float:
    """Score a deal, tagging the log line with the request's correlation id."""
    _logger.info(f"[{correlation_id}] Scoring deal: {deal['deal_name']}")
    return deal["market_value"] * 0.05


def process_deal_request(deal_name: str) -> dict:
    """Handle one full request, threading a single correlation id throughout."""
    correlation_id = start_request()
    deal = fetch_deal(deal_name, correlation_id)
    score = score_deal(deal, correlation_id)
    return {"deal": deal, "score": score, "correlation_id": correlation_id}


if __name__ == "__main__":
    result = process_deal_request("Riverside JV")
    print(result)

    # a second, concurrent-looking request gets its own distinct id
    result2 = process_deal_request("Westgate Retail")
    print(result2)
    assert result["correlation_id"] != result2["correlation_id"]