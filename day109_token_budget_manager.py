"""Day 109 - Rate Limiting and Token Budget Management: Token Budget Manager.

Tracks token usage within a rolling one-minute window and refuses new
requests once the budget is exhausted, rather than relying on the API
to reject them - PCPP1 standard.
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

_WINDOW_SECONDS = 60


class TokenBudget:
    """Tracks cumulative token spend within a rolling time window."""

    def __init__(self, max_tokens_per_minute: int) -> None:
        self.max_tokens_per_minute = max_tokens_per_minute
        self.used_tokens = 0
        self.window_start = time.time()

    def _reset_if_new_window(self) -> None:
        """Reset the counter if the current window has elapsed."""
        if time.time() - self.window_start > _WINDOW_SECONDS:
            self.used_tokens = 0
            self.window_start = time.time()

    def can_spend(self, tokens: int) -> bool:
        """Return whether spending this many tokens stays within budget."""
        self._reset_if_new_window()
        return self.used_tokens + tokens <= self.max_tokens_per_minute

    def record_spend(self, tokens: int) -> None:
        """Add newly spent tokens to the running total for this window."""
        self._reset_if_new_window()
        self.used_tokens += tokens

    def remaining(self) -> int:
        """Return the tokens still available in the current window."""
        self._reset_if_new_window()
        return self.max_tokens_per_minute - self.used_tokens


def ask_within_budget(budget: TokenBudget, question: str, estimated_tokens: int) -> str:
    """Ask a question only if it fits within the remaining token budget."""
    if not budget.can_spend(estimated_tokens):
        return f"Budget exceeded, request skipped. Remaining: {budget.remaining()}"

    response = _client.messages.create(
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
    print(f"Remaining budget: {budget.remaining()}")