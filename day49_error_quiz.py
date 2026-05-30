# Day 49 - Error Finding Quiz

import functools

class CountCalls:

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count =+ 1              # Bug 1 - wrong operator, should be +=
        return self.func(*args, **kwargs)


class RetryOnError:

    def __init__(self, retries=3):
        self.retries = retries

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper   # correct


class RateLimit:

    def __init__(self, max_calls):
        max_calls = max_calls        # Bug 2 - missing self
        self.calls = 0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.calls >= self.max_calls:
                raise RuntimeError("Rate limit exceeded.")
            self.calls += 1
            return func(*args, **kwargs)
        return wrapper


@CountCalls
def greet(name):
    """Greet someone."""
    return f"Hello, {name}!"


print(greet("Alice"))
print(greet("Bob"))
print(greet.count)            # Bug 3 - count is wrong due to Bug 1
print(greet.__name__)