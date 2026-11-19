"""Day 212 - Context-Window Packing for RAG prompts.

A prompt has a fixed token budget: the model's context limit MINUS the
tokens reserved for its answer MINUS the fixed prompt overhead. Chunks
are taken most-relevant first; one that does not fit is SKIPPED (a
smaller, lower-ranked chunk may still fit), and the chosen chunks are
put back in DOCUMENT order so the text reads coherently - PCPP1 standard.
Token counting here is a simple word count; a real system uses the
model's own tokenizer.
"""
from __future__ import annotations


def count_tokens(text: str) -> int:
    """Approximate token count: one per whitespace-separated word."""
    return len(text.split())


def pack_chunks(
    chunks: list[dict], context_limit: int, reserved_for_output: int, prompt_overhead: int
) -> tuple[list[dict], int]:
    """Return (chosen chunks in document order, tokens used)."""
    budget = context_limit - reserved_for_output - prompt_overhead
    if budget <= 0:
        raise ValueError("no token budget left for any context")

    chosen: list[dict] = []
    used = 0
    for chunk in sorted(chunks, key=lambda c: c["score"], reverse=True):
        tokens = count_tokens(chunk["text"])
        if used + tokens > budget:
            continue
        chosen.append(chunk)
        used += tokens
    chosen.sort(key=lambda c: c["position"])
    return chosen, used


if __name__ == "__main__":
    chunks = [
        {"id": "c1", "position": 0, "score": 0.90, "text": "one two three four five six seven eight"},
        {"id": "c2", "position": 1, "score": 0.70, "text": "one two three four five six"},
        {"id": "c3", "position": 2, "score": 0.95, "text": "one two three four five six seven eight nine ten"},
        {"id": "c4", "position": 3, "score": 0.80, "text": "one two three four"},
        {"id": "c5", "position": 4, "score": 0.85, "text": "one two three four five"},
        {"id": "c6", "position": 5, "score": 0.60, "text": "one two three"},
    ]
    chosen, used = pack_chunks(chunks, context_limit=40, reserved_for_output=10, prompt_overhead=8)
    print([c["id"] for c in chosen], used)