"""Day 103 - Agentic Tool Use: Deal Lookup Agent.

Defines a single tool the model can call to look up a deal's LTV,
sends the tool result back to the model for a natural-language
answer, and handles unknown deal ids gracefully - PCPP1 standard.
"""
from __future__ import annotations

import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)

_DEALS: dict[str, dict] = {
    "riverside-jv": {"market_value": 12_500_000.0, "ltv": 0.60},
    "logistics-portfolio": {"market_value": 34_200_000.0, "ltv": 0.55},
}

_TOOLS = [
    {
        "name": "get_deal_ltv",
        "description": "Get the loan-to-value ratio for a named deal.",
        "input_schema": {
            "type": "object",
            "properties": {
                "deal_id": {"type": "string", "description": "The deal identifier."},
            },
            "required": ["deal_id"],
        },
    }
]


def get_deal_ltv(deal_id: str) -> dict:
    """Look up a deal's LTV, raising a clear error if it doesn't exist."""
    if deal_id not in _DEALS:
        return {"error": f"No deal found with id '{deal_id}'"}
    deal = _DEALS[deal_id]
    return {"deal_id": deal_id, "ltv": deal["ltv"]}


def run_agent(question: str) -> str:
    """Answer a question, calling the LTV tool when the model requests it."""
    messages: list[dict] = [{"role": "user", "content": question}]

    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        tools=_TOOLS,
        messages=messages,
    )

    if response.stop_reason == "tool_use":
        tool_block = next(b for b in response.content if b.type == "tool_use")
        result = get_deal_ltv(tool_block.input["deal_id"])

        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": str(result),
                }
            ],
        })

        follow_up = _client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            tools=_TOOLS,
            messages=messages,
        )
        return follow_up.content[0].text

    return response.content[0].text


if __name__ == "__main__":
    print(run_agent("What is the LTV of riverside-jv?"))