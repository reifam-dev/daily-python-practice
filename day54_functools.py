# Day 54 - Clean functools module examples
# New concepts: lru_cache, cache_info, cache_clear, partial, reduce
# PEP 8, docstrings, type hints, exceptions throughout

import functools
from typing import List, Callable, TypeVar

T = TypeVar('T')


@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number using lru_cache for memoisation.

    lru_cache stores results of previous calls — repeated calls are
    returned instantly from the cache without recomputation.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative. Got {n}.")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def power(base: float, exponent: float) -> float:
    """Return base raised to exponent."""
    return base ** exponent


# functools.partial — pre-fills arguments to create specialised functions
square: Callable[[float], float] = functools.partial(power, exponent=2)
cube: Callable[[float], float] = functools.partial(power, exponent=3)
double: Callable[[float], float] = functools.partial(power, exponent=1)


@functools.lru_cache(maxsize=None)
def factorial(n: int) -> int:
    """Return n! using lru_cache for memoisation.

    Module-level function — lru_cache works correctly here.
    Avoid using lru_cache directly on instance methods.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative. Got {n}.")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


if __name__ == "__main__":
    print("=== lru_cache — Fibonacci ===\n")
    print(f"  fibonacci(35)  = {fibonacci(35)}")
    print(f"  Cache info     : {fibonacci.cache_info()}")
    fibonacci.cache_clear()
    print(f"  After clear    : {fibonacci.cache_info()}\n")

    print("=== functools.partial ===\n")
    print(f"  square(5)      = {square(5):.1f}")
    print(f"  square(12)     = {square(12):.1f}")
    print(f"  cube(3)        = {cube(3):.1f}")
    print(f"  double(7)      = {double(7):.1f}\n")

    print("=== functools.reduce ===\n")
    numbers: List[int] = [1, 2, 3, 4, 5]
    product = functools.reduce(lambda acc, x: acc * x, numbers)
    total = functools.reduce(lambda acc, x: acc + x, numbers, 0)
    maximum = functools.reduce(lambda acc, x: acc if acc > x else x, numbers)
    print(f"  Product : {product}")
    print(f"  Sum     : {total}")
    print(f"  Maximum : {maximum}")

    safe = functools.reduce(lambda acc, x: acc + x, [], 0)
    print(f"  Empty with initial=0: {safe}\n")

    print("=== lru_cache — factorial ===\n")
    for n in [5, 10, 5, 10]:
        print(f"  factorial({n}) = {factorial(n)}")
    print(f"  Cache info: {factorial.cache_info()}\n")

    try:
        functools.reduce(lambda acc, x: acc + x, [])
    except TypeError as e:
        print(f"  reduce on empty list no initial: TypeError: {e}")