"""Day 104 - Structured Data Extraction: Deal Extractor.

Uses Pydantic's schema generation to define a tool that forces the
model to return structured, validated deal data from free-text
descriptions - PCPP1 standard.
"""
from __future__ import annotations

import os

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)


class DealExtract(BaseModel):
    """Structured representation of a deal extracted from free text."""

    deal_name: str
    market_value: float
    ltv: float
    sector: str


_EXTRACTION_TOOL = {
    "name": "record_deal",
    "description": "Record structured deal data extracted from free text.",
    "input_schema": DealExtract.model_json_schema(),
}


class ExtractionError(Exception):
    """Raised when the model's tool output fails schema validation."""


def extract_deal(raw_text: str) -> DealExtract:
    """Extract structured deal data from a free-text description."""
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        tools=[_EXTRACTION_TOOL],
        tool_choice={"type": "tool", "name": "record_deal"},
        messages=[{"role": "user", "content": f"Extract deal data from: {raw_text}"}],
    )
    tool_block = next(b for b in response.content if b.type == "tool_use")

    try:
        return DealExtract(**tool_block.input)
    except ValidationError as exc:
        raise ExtractionError(f"Model output failed validation: {exc}") from exc


if __name__ == "__main__":
    text = "Riverside JV is a logistics deal valued at 12.5m with 60% LTV."
    deal = extract_deal(text)
    print(deal.deal_name, deal.market_value, deal.ltv, deal.sector)