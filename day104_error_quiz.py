"""Day 104 - Structured Data Extraction: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)


class DealExtract(BaseModel):
    deal_name: str
    market_value: float
    ltv: float
    sector: str


EXTRACTION_TOOL = {
    "name": "record_deal",
    "description": "Record structured deal data extracted from free text.",
    "input_schema": DealExtract.schema(),
}


def extract_deal(raw_text: str) -> DealExtract:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        tools=[EXTRACTION_TOOL],
        tool_choice={"type": "tool"},
        messages=[{"role": "user", "content": f"Extract deal data from: {raw_text}"}],
    )
    tool_block = next(b for b in response.content if b.type == "tool_use")
    return DealExtract(tool_block.input)


if __name__ == "__main__":
    text = "Riverside JV is a logistics deal valued at 12.5m with 60% LTV."
    deal = extract_deal(text)
    print(deal.deal_name, deal.market_value, deal.ltv, deal.sector)