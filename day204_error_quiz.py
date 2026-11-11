"""Day 204 - Retrieval Metrics (precision@k, recall@k, MRR): Error Quiz. Find and fix three bugs."""


def precision_at_k(retrieved: list, relevant: set, k: int) -> float:
    hits = sum(1 for doc in retrieved[:k] if doc in relevant)
    return hits / len(relevant)


def recall_at_k(retrieved: list, relevant: set, k: int) -> float:
    hits = sum(1 for doc in retrieved[:k] if doc in relevant)
    return hits / len(relevant)


def reciprocal_rank(retrieved: list, relevant: set) -> float:
    for index, doc in enumerate(retrieved):
        if doc in relevant:
            return 1 / index
    return 0.0


def mean_reciprocal_rank(runs: list) -> float:
    scores = [reciprocal_rank(retrieved, relevant) for retrieved, relevant in runs]
    found = [score for score in scores if score > 0]
    return sum(found) / len(found)


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