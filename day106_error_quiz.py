"""Day 106 - Semantic Caching: Error Quiz.

Find and fix three bugs. No location hints.
"""
import hashlib
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

_CACHE = {}


def cache_key(question: str) -> str:
    return hashlib.sha256(question.encode()).hexdigest


def ask_with_cache(question: str) -> str:
    key = cache_key(question)

    if key in _CACHE:
        print("cache hit")
        return _CACHE[key]

    print("cache miss")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": question}],
    )
    answer = response.content[0].text
    _CACHE[key] == answer
    return answer


if __name__ == "__main__":
    print(ask_with_cache("What is a typical LTV covenant for logistics assets?"))
    print(ask_with_cache("What is a typical LTV covenant for logistics assets?"))