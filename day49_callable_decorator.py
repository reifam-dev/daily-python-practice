# Day 49 - Clean class-based decorators using __call__
# New concepts: __call__, class-based decorator, functools.update_wrapper
# PEP 8, docstrings, type hints, exceptions throughout

import functools
from typing import Callable, Any


class CountCalls:
    """Class-based decorator that counts how many times a function is called.

    Uses __call__ to make the instance callable.
    functools.update_wrapper preserves __name__, __doc__ etc.
    """

    def __init__(self, func: Callable) -> None:
        functools.update_wrapper(self, func)
        self._func = func
        self.count: int = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Increment count and call the wrapped function."""
        self.count += 1
        return self._func(*args, **kwargs)

    def reset(self) -> None:
        """Reset the call count to zero."""
        self.count = 0


class RetryOnError:
    """Class-based decorator factory — retries a function on exception.

    Usage: @RetryOnError(retries=3)
    """

    def __init__(self, retries: int = 3) -> None:
        self._retries = retries

    def __call__(self, func: Callable) -> Callable:
        """Return a wrapper that retries on exception."""
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, self._retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  Attempt {attempt}/{self._retries} failed: {e}")
            print(f"  All {self._retries} attempts failed.")
            return None
        return wrapper


class RateLimit:
    """Class-based decorator factory — limits number of calls.

    Usage: @RateLimit(max_calls=3)
    """

    def __init__(self, max_calls: int) -> None:
        self._max_calls = max_calls
        self._calls: int = 0

    def __call__(self, func: Callable) -> Callable:
        """Return a wrapper that enforces the rate limit."""
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if self._calls >= self._max_calls:
                raise RuntimeError(
                    f"Rate limit of {self._max_calls} calls exceeded "
                    f"for '{func.__name__}'."
                )
            self._calls += 1
            return func(*args, **kwargs)
        return wrapper


@CountCalls
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"


@RetryOnError(retries=3)
def unstable_operation(x: int) -> int:
    """Simulates an operation that sometimes fails."""
    if x < 3:
        raise ValueError(f"Value {x} is too small.")
    return x * 10


@RateLimit(max_calls=3)
def fetch_data(endpoint: str) -> str:
    """Simulates a rate-limited API call."""
    return f"Data from {endpoint}"


if __name__ == "__main__":
    print("=== CountCalls class-based decorator ===\n")
    print(f"  {greet('Alice')}")
    print(f"  {greet('Bob')}")
    print(f"  {greet('Charlie')}")
    print(f"  Call count      : {greet.count}")
    print(f"  Function name   : {greet.__name__}")
    print(f"  Docstring       : {greet.__doc__}")

    greet.reset()
    print(f"  After reset     : {greet.count}\n")

    print("=== RetryOnError class-based decorator ===\n")
    result = unstable_operation(1)
    print(f"  Result: {result}\n")
    result = unstable_operation(5)
    print(f"  Result: {result}\n")

    print("=== RateLimit class-based decorator ===\n")
    try:
        for i in range(5):
            print(f"  {fetch_data(f'/api/endpoint/{i}')}")
    except RuntimeError as e:
        print(f"  Error: {e}")