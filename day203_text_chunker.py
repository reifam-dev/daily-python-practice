"""Day 203 - Text Chunking with Overlap, for RAG.

Documents are split into chunks of chunk_size words. Consecutive chunks
share `overlap` words so a sentence cut at a boundary still appears whole
in one of them. The window advances by (chunk_size - overlap), the final
partial window is KEPT (nothing is silently dropped), a text shorter than
one chunk still yields one chunk, and impossible settings are rejected
(an overlap of chunk_size or more would never advance) - PCPP1 standard.
"""
from __future__ import annotations


def chunk_words(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping word chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be at least 0 and less than chunk_size")

    words = text.split()
    if not words:
        return []

    step = chunk_size - overlap
    chunks: list[str] = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + chunk_size]))
        if start + chunk_size >= len(words):
            break
    return chunks


if __name__ == "__main__":
    text = " ".join(f"w{i}" for i in range(20))
    chunks = chunk_words(text, chunk_size=8, overlap=2)
    for chunk in chunks:
        print(chunk)
    print(chunk_words("only five words in this", chunk_size=8, overlap=2))

    covered = {word for chunk in chunks for word in chunk.split()}
    assert covered == set(text.split()), "every word must appear in at least one chunk"
    try:
        chunk_words(text, chunk_size=8, overlap=8)
    except ValueError as exc:
        print(f"Rejected: {exc}")