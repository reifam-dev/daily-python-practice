"""Day 111 - Structured Logging and Observability: Observable Deal Agent.

Logs every LLM call as a structured JSON record (question, answer,
latency, token usage) rather than free-text messages, making calls
searchable and analysable downstream - PCPP1 standard.
"""
from __future__ import annotations

import json
import logging
import os
import time

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)

_logger = logging.getLogger("deal_agent")
_logger.setLevel(logging.INFO)
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _logger.addHandler(_handler)


def log_llm_call(question: str, answer: str, duration_ms: float, tokens: int) -> None:
    """Log a single LLM call as a structured JSON record."""
    record = {
        "question": question,
        "answer": answer,
        "duration_ms": round(duration_ms, 2),
        "tokens": tokens,
    }
    _logger.info(json.dumps(record))


def ask_with_observability(question: str) -> str:
    """Ask a question and log the call's latency and token usage."""
    start = time.time()
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": question}],
    )
    duration_ms = (time.time() - start) * 1000
    answer = response.content[0].text
    log_llm_call(question, answer, duration_ms, response.usage.output_tokens)
    return answer


if __name__ == "__main__":
    print(ask_with_observability("What is a typical LTV covenant for logistics assets?"))