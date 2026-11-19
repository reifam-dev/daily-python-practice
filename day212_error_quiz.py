"""Day 212 - Context-Window Packing: Error Quiz. Find and fix three bugs."""


def count_tokens(text: str) -> int:
    return len(text.split())


def pack_chunks(chunks: list, context_limit: int, reserved_for_output: int, prompt_overhead: int):
    budget = context_limit - prompt_overhead
    chosen = []
    used = 0
    for chunk in sorted(chunks, key=lambda c: c["score"], reverse=True):
        tokens = count_tokens(chunk["text"])
        if used + tokens > budget:
            break
        chosen.append(chunk)
        used += tokens
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