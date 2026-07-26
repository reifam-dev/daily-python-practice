"""Day 107 - Retry Logic and Exponential Backoff: Resilient Deal Client.

Retries transient API failures with exponential backoff, distinguishes
retryable errors (rate limits, server errors) from non-retryable ones,
and gives up gracefully after a fixed number of attempts - PCPP1
standard.
"""
from __future__ import annotations

import os
import time

from anthropic import Anthropic, APIStatusError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)

_MAX_RETRIES = 3
_BASE_DELAY_SECONDS = 1.0


class RetriesExhaustedError(Exception):
    """Raised when all retry attempts have been used without success."""


def call_with_retry(question: str) -> str:
    """Call the API, retrying transient failures with exponential backoff."""
    last_error: Exception | None = None

    for attempt in range(_MAX_RETRIES):
        try:
            response = _client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=300,
                messages=[{"role": "user", "content": question}],
            )
            return response.content[0].text
        except RateLimitError as exc:
            last_error = exc
            delay = _BASE_DELAY_SECONDS * (2 ** attempt)
            print(f"Rate limited, retrying in {delay}s...")
            time.sleep(delay)
        except APIStatusError as exc:
            if exc.status_code >= 500:
                last_error = exc
                delay = _BASE_DELAY_SECONDS * (2 ** attempt)
                print(f"Server error ({exc.status_code}), retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise

    raise RetriesExhaustedError(
        f"Failed after {_MAX_RETRIES} attempts: {last_error}"
    ) from last_error


if __name__ == "__main__":
    print(call_with_retry("What is a typical LTV covenant for logistics assets?"))