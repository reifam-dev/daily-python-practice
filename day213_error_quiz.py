"""Day 213 - Reciprocal Rank Fusion: Error Quiz. Find and fix three bugs."""


def reciprocal_rank_fusion(rankings: list, k: int = 60) -> list:
    shared = set.intersection(*(set(ranking) for ranking in rankings))
    scores = {}
    for ranking in rankings:
        for rank, doc in enumerate(ranking, start=1):
            if doc in shared:
                scores[doc] = 1.0 / (k + rank)
    return sorted(scores, key=lambda doc: scores[doc])


if __name__ == "__main__":
    keyword = ["d3", "d1", "d7", "d2"]
    vector = ["d1", "d9", "d3", "d4"]
    print(reciprocal_rank_fusion([keyword, vector]))