"""Day 155 - Memoization: caches each subproblem's result so it's
computed exactly once, turning exponential recursive Fibonacci into
linear time. A mutable default argument is deliberately avoided -
cache is passed explicitly - PCPP1 standard."""
from __future__ import annotations


def fibonacci(n: int, cache: dict | None = None) -> int:
    if cache is None:
        cache = {}
    if n <= 1:
        return n
    if n in cache:
        return cache[n]

    result = fibonacci(n - 1, cache) + fibonacci(n - 2, cache)
    cache[n] = result
    return result


if __name__ == "__main__":
    import time

    start = time.time()
    print(fibonacci(30))
    print(f"Took {time.time() - start:.4f}s")