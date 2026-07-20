"""Day 101 - Prompt Engineering: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

SYSTEM_PROMPT = """You are a real estate investment analyst. Answer only
using the deal information provided in the user's message. If the
information needed is not present, say so explicitly rather than
guessing."""


def build_few_shot_prompt(deal_summary: str, question: str) -> str:
    examples = (
        "Example:\n"
        "Deal: LTV 55%, yield 6.1%.\n"
        "Question: Is this deal within a 65% LTV covenant?\n"
        "Answer: Yes, 55% is within the 65% covenant.\n\n"
    )
    return examples + f"Deal: {deal_summary}\nQuestion: {question}\nAnswer:"


def ask_analyst(deal_summary: str, question: str) -> str:
    prompt = build_few_shot_prompt(deal_summary, question)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        temperature=1.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content


if __name__ == "__main__":
    answer = ask_analyst(
        "LTV 72%, yield 5.4%, sector: logistics.",
        "Is this deal within a 65% LTV covenant?",
    )
    print(answer)