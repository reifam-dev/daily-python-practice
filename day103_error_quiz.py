"""Day 103 - Agentic Tool Use: Error Quiz.

Find and fix three bugs. No location hints.
"""
import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

DEALS = {
    "riverside-jv": {"market_value": 12_500_000.0, "ltv": 0.60},
    "logistics-portfolio": {"market_value": 34_200_000.0, "ltv": 0.55},
}

TOOLS = [
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
    deal = DEALS[deal_id]
    return {"deal_id": deal_id, "ltv": deal["ltv"]}


def run_agent(question: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        tools=TOOLS,
        messages=[{"role": "user", "content": question}],
    )

    if response.stop_reason = "tool_use":
        tool_block = next(b for b in response.content if b.type == "tool_use")
        result = get_deal_ltv(tool_block.input["deal_id"])
        return json.dumps(result)

    return response.content[0].text


if __name__ == "__main__":
    print(run_agent("What is the LTV of riverside-jv?"))