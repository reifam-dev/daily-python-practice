"""Day 155 - Memoization: Error Quiz. Find and fix three bugs."""
def fibonacci(n: int, cache: dict = {}) -> int:
    if n <= 1:
        return n
    if n in cache:
        return cache[n]

    result = fibonacci(n - 1) + fibonacci(n - 2)
    return result


if __name__ == "__main__":
    import time

    start = time.time()
    print(fibonacci(30))
    print(f"Took {time.time() - start:.4f}s")