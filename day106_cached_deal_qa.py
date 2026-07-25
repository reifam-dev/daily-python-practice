"""Day 106 - Semantic Caching: Cached Deal Q&A.

Caches exact-match question/answer pairs by hashing the normalised
question text, avoiding repeat API calls for identical questions -
PCPP1 standard.
"""
from __future__ import annotations

import hashlib
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)

_cache: dict[str, str] = {}


def cache_key(question: str) -> str:
    """Return a stable hash key for a normalised question string."""
    normalised = question.strip().lower()
    return hashlib.sha256(normalised.encode()).hexdigest()


def ask_with_cache(question: str) -> str:
    """Answer a question, serving from cache on repeat questions."""
    key = cache_key(question)

    if key in _cache:
        print("cache hit")
        return _cache[key]

    print("cache miss")
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": question}],
    )
    answer = response.content[0].text
    _cache[key] = answer
    return answer


def cache_size() -> int:
    """Return the number of distinct questions currently cached."""
    return len(_cache)


if __name__ == "__main__":
    print(ask_with_cache("What is a typical LTV covenant for logistics assets?"))
    print(ask_with_cache("What is a typical LTV covenant for logistics assets?"))
    print(f"Cache entries: {cache_size()}")