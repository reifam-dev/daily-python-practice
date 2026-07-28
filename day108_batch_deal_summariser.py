"""Day 108 - Batch Processing: Batch Deal Summariser.

Submits multiple deal-summary requests as a single Message Batch,
polls until processing completes, and maps each result back to its
originating deal via custom_id - PCPP1 standard.
"""
from __future__ import annotations

import os
import time

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)

_POLL_INTERVAL_SECONDS = 2

_DEALS: list[str] = [
    "Riverside JV, 12.5m, logistics, 60% LTV.",
    "Westgate Retail, 8.1m, retail, 65% LTV.",
    "Docklands Logistics, 15.75m, logistics, 55% LTV.",
]


def build_batch_requests(deals: list[str]) -> list[dict]:
    """Build one batch request per deal, each tagged with a custom_id."""
    requests = []
    for i, deal in enumerate(deals):
        requests.append({
            "custom_id": f"deal-{i}",
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 200,
                "messages": [{"role": "user", "content": f"Summarise in one sentence: {deal}"}],
            },
        })
    return requests


def run_batch(deals: list[str]) -> dict[str, str]:
    """Submit a batch, poll until complete, and return results keyed by custom_id."""
    requests = build_batch_requests(deals)
    batch = _client.messages.batches.create(requests=requests)

    while batch.processing_status == "in_progress":
        time.sleep(_POLL_INTERVAL_SECONDS)
        batch = _client.messages.batches.retrieve(batch.id)

    results: dict[str, str] = {}
    for entry in _client.messages.batches.results(batch.id):
        if entry.result.type == "succeeded":
            results[entry.custom_id] = entry.result.message.content[0].text
        else:
            results[entry.custom_id] = f"[failed: {entry.result.type}]"

    return results


if __name__ == "__main__":
    outcomes = run_batch(_DEALS)
    for deal_id, summary in outcomes.items():
        print(deal_id, summary)