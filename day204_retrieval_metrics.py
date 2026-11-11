"""Day 204 - Retrieval Metrics: how good is the retriever, in numbers?

precision@k = relevant documents in the top k / k   (how much of what
we showed was useful). recall@k = relevant documents in the top k /
ALL relevant documents   (how much of what existed did we find).
Reciprocal rank = 1 / the 1-based rank of the first relevant document,
or 0 if none was retrieved; MRR averages it over ALL queries, including
the ones that found nothing - PCPP1 standard.
"""
from __future__ import annotations


def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """Fraction of the top k results that are relevant (short lists are penalised)."""
    if k <= 0:
        raise ValueError("k must be positive")
    hits = sum(1 for doc in retrieved[:k] if doc in relevant)
    return hits / k


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """Fraction of all relevant documents found in the top k."""
    if k <= 0:
        raise ValueError("k must be positive")
    if not relevant:
        raise ValueError("relevant must not be empty")
    hits = sum(1 for doc in retrieved[:k] if doc in relevant)
    return hits / len(relevant)


def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    """1 / rank of the first relevant result, ranks starting at 1; 0 if none."""
    for rank, doc in enumerate(retrieved, start=1):
        if doc in relevant:
            return 1 / rank
    return 0.0


def mean_reciprocal_rank(runs: list[tuple[list[str], set[str]]]) -> float:
    """Average reciprocal rank over every query, misses counting as 0."""
    if not runs:
        raise ValueError("runs must not be empty")
    scores = [reciprocal_rank(retrieved, relevant) for retrieved, relevant in runs]
    return sum(scores) / len(scores)


if __name__ == "__main__":
    runs = [
        (["d3", "d1", "d7", "d2"], {"d1", "d2"}),
        (["d5", "d6", "d4"], {"d4"}),
        (["d8", "d9"], {"d1"}),
    ]
    print(round(precision_at_k(*runs[0], 3), 4))
    print(round(recall_at_k(*runs[0], 3), 4))
    print(round(reciprocal_rank(*runs[1]), 4))
    print(round(mean_reciprocal_rank(runs), 4))