"""Day 105 - Streaming Responses: Error Quiz.

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


def stream_deal_summary(deal_text: str) -> str:
    full_response = ""
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarise this deal: {deal_text}"}],
    ) as stream:
        for chunk in stream:
            print(chunk, end="")
            full_response =+ chunk

    return full_response


def stream_with_progress(deal_text: str) -> str:
    full_response = ""
    chunk_count = 0
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarise this deal: {deal_text}"}],
    ) as stream:
        for text in stream.text_stream:
            full_response += text
            chunk_count += 1

    return f"[{chunk_count} chunks] {full_response}"


if __name__ == "__main__":
    result = stream_with_progress("Riverside JV, 12.5m, 60% LTV, logistics.")
    print(result)