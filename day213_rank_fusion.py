"""Day 213 - Reciprocal Rank Fusion: merging keyword and vector search.

Each ranked list gives a document 1 / (k + rank) (ranks start at 1), and
a document's fused score is the SUM across every list it appears in, so
agreement between retrievers is rewarded. A document found by only one
retriever is kept (it still scores), results are ordered best first, and
ties break alphabetically so the output is deterministic - PCPP1
standard.
"""
from __future__ import annotations


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Fuse ranked lists into one list of (document, score), best first."""
    if k <= 0:
        raise ValueError("k must be positive")
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc in enumerate(ranking, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))


if __name__ == "__main__":
    keyword = ["d3", "d1", "d7", "d2"]
    vector = ["d1", "d9", "d3", "d4"]
    for doc, score in reciprocal_rank_fusion([keyword, vector]):
        print(doc, round(score, 5))