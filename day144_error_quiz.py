"""Day 144 - Rate Limiter Algorithms: Error Quiz.

Find and fix three bugs. No location hints.
"""
import time


class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_rate_per_second: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_second
        self.tokens = capacity
        self.last_refill = time.time()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        added = elapsed * self.refill_rate
        self.tokens = self.tokens + added
        self.last_refill = now

    def allow_request(self) -> bool:
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class SlidingWindowLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_times = []

    def allow_request(self) -> bool:
        now = time.time()
        self.request_times = [t for t in self.request_times if now - t < self.window_seconds]

        if len(self.request_times) < self.max_requests:
            return True
        return False


if __name__ == "__main__":
    bucket = TokenBucketLimiter(capacity=3, refill_rate_per_second=1.0)
    for i in range(5):
        print(f"Token bucket request {i}: {bucket.allow_request()}")

    window = SlidingWindowLimiter(max_requests=3, window_seconds=10.0)
    for i in range(5):
        print(f"Sliding window request {i}: {window.allow_request()}")