"""Day 126 - Distributed Tracing with Correlation IDs: Error Quiz.

Find and fix three bugs. No location hints.
"""
import logging
import uuid

logger = logging.getLogger("deal_pipeline")
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())

_current_correlation_id = None


def start_request() -> str:
    correlation_id = uuid.uuid4()
    return correlation_id


def fetch_deal(deal_name: str) -> dict:
    logger.info(f"Fetching deal: {deal_name}")
    return {"deal_name": deal_name, "market_value": 12_500_000.0}


def score_deal(deal: dict) -> float:
    logger.info(f"Scoring deal: {deal['deal_name']}")
    return deal["market_value"] * 0.05


def process_deal_request(deal_name: str) -> dict:
    correlation_id = start_request()
    deal = fetch_deal(deal_name)
    score = score_deal(deal)
    return {"deal": deal, "score": score, "correlation_id": correlation_id}


if __name__ == "__main__":
    result = process_deal_request("Riverside JV")
    print(result)