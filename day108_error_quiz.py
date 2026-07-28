"""Day 108 - Batch Processing: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os
import time

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

DEALS = [
    "Riverside JV, 12.5m, logistics, 60% LTV.",
    "Westgate Retail, 8.1m, retail, 65% LTV.",
    "Docklands Logistics, 15.75m, logistics, 55% LTV.",
]


def build_batch_requests(deals: list[str]) -> list[dict]:
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


def run_batch(deals: list[str]) -> dict:
    requests = build_batch_requests(deals)
    batch = client.messages.batches.create(requests)

    while batch.processing_status == "in_progress":
        time.sleep(2)
        batch = client.messages.batches.retrieve(batch.id)

    results = {}
    for entry in client.messages.batches.results(batch.id):
        results[entry.custom_id] = entry.result.message.content

    return results


if __name__ == "__main__":
    outcomes = run_batch(DEALS)
    for deal_id, summary in outcomes.items():
        print(deal_id, summary)