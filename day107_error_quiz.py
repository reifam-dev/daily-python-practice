"""Day 107 - Retry Logic and Exponential Backoff: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os
import time

from anthropic import Anthropic, APIStatusError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

MAX_RETRIES = 3
BASE_DELAY_SECONDS = 1.0


def call_with_retry(question: str) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=300,
                messages=[{"role": "user", "content": question}],
            )
            return response.content[0].text
        except RateLimitError:
            delay = BASE_DELAY_SECONDS * attempt
            print(f"Rate limited, retrying in {delay}s...")
            time.sleep(delay)
        except APIStatusError as exc:
            print(f"API error: {exc}")

    return "Failed after retries"


if __name__ == "__main__":
    print(call_with_retry("What is a typical LTV covenant for logistics assets?"))