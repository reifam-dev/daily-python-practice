"""Day 105 - Streaming Responses: Deal Summary Streamer.

Uses the Anthropic streaming API to print a deal summary token by
token as it arrives, while also accumulating the full text and a
running chunk count - PCPP1 standard.
"""
from __future__ import annotations

import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)


def stream_deal_summary(deal_text: str, show_progress: bool = True) -> str:
    """Stream a deal summary, printing tokens live and returning the full text."""
    full_response = ""

    with _client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarise this deal: {deal_text}"}],
    ) as stream:
        for text in stream.text_stream:
            if show_progress:
                print(text, end="", flush=True)
            full_response += text

    if show_progress:
        print()

    return full_response


def stream_with_chunk_count(deal_text: str) -> tuple[str, int]:
    """Stream a summary and return both the full text and chunk count."""
    full_response = ""
    chunk_count = 0

    with _client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarise this deal: {deal_text}"}],
    ) as stream:
        for text in stream.text_stream:
            full_response += text
            chunk_count += 1

    return full_response, chunk_count


if __name__ == "__main__":
    summary, count = stream_with_chunk_count("Riverside JV, 12.5m, 60% LTV, logistics.")
    print(f"\n[{count} chunks] {summary}")