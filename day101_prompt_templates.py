"""Day 101 - Prompt Engineering: Deal Analyst Prompt Templates.

Demonstrates a system prompt, a few-shot user prompt builder, and
low-temperature, deterministic-leaning generation for a factual
analysis task - PCPP1 standard.
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

_SYSTEM_PROMPT = """You are a real estate investment analyst. Answer only
using the deal information provided in the user's message. If the
information needed is not present, say so explicitly rather than
guessing."""

_FEW_SHOT_EXAMPLE = (
    "Example:\n"
    "Deal: LTV 55%, yield 6.1%.\n"
    "Question: Is this deal within a 65% LTV covenant?\n"
    "Answer: Yes, 55% is within the 65% covenant.\n\n"
)


def build_few_shot_prompt(deal_summary: str, question: str) -> str:
    """Build a one-shot prompt anchoring the model's answer format."""
    return f"{_FEW_SHOT_EXAMPLE}Deal: {deal_summary}\nQuestion: {question}\nAnswer:"


def ask_analyst(deal_summary: str, question: str) -> str:
    """Ask a factual question about a deal, using a low temperature
    to keep answers consistent and grounded rather than creative."""
    prompt = build_few_shot_prompt(deal_summary, question)
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        temperature=0.0,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    answer = ask_analyst(
        "LTV 72%, yield 5.4%, sector: logistics.",
        "Is this deal within a 65% LTV covenant?",
    )
    print(answer)