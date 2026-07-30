"""Day 111 - Structured Logging and Observability: Error Quiz.

Find and fix three bugs. No location hints.
"""
import json
import logging
import os
import time

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

logger = logging.getLogger("deal_agent")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)


def log_llm_call(question: str, answer: str, duration_ms: float, tokens: int) -> None:
    record = {
        "question": question,
        "answer": answer,
        "duration_ms": duration_ms,
        "tokens": tokens,
    }
    logger.info(record)


def ask_with_observability(question: str) -> str:
    start = time.time()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": question}],
    )
    duration_ms = time.time() - start
    answer = response.content[0].text
    log_llm_call(question, answer, duration_ms, response.usage.output_tokens)
    return answer


if __name__ == "__main__":
    print(ask_with_observability("What is a typical LTV covenant for logistics assets?"))