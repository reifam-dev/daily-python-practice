"""Day 109 - Rate Limiting and Token Budget Management: Error Quiz.

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


class TokenBudget:
    def __init__(self, max_tokens_per_minute: int):
        self.max_tokens_per_minute = max_tokens_per_minute
        self.used_tokens = 0
        self.window_start = time.time()

    def _reset_if_new_window(self) -> None:
        if time.time() - self.window_start > 60:
            self.used_tokens = 0
            self.window_start = time.time()

    def can_spend(self, tokens: int) -> bool:
        self._reset_if_new_window()
        return self.used_tokens + tokens < self.max_tokens_per_minute

    def record_spend(self, tokens: int):
        self.used_tokens = tokens


def ask_within_budget(budget: TokenBudget, question: str, estimated_tokens: int) -> str:
    if not budget.can_spend(estimated_tokens):
        return "Budget exceeded, request skipped."

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=estimated_tokens,
        messages=[{"role": "user", "content": question}],
    )
    budget.record_spend(response.usage.output_tokens)
    return response.content[0].text


if __name__ == "__main__":
    budget = TokenBudget(max_tokens_per_minute=1000)
    print(ask_within_budget(budget, "What is a typical LTV covenant?", 200))
    print(ask_within_budget(budget, "What is a typical yield for logistics?", 200))