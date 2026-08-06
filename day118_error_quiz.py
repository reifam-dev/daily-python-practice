"""Day 118 - Circuit Breaker Pattern: Error Quiz.

Find and fix three bugs. No location hints.
"""
import time


class CircuitBreaker:
    def __init__(self, failure_threshold: int, cooldown_seconds: float):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.failure_count = 0
        self.state = "closed"
        self.opened_at = None

    def _should_attempt_reset(self) -> bool:
        return time.time() - self.opened_at > self.cooldown_seconds

    def call(self, func, *args):
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half_open"
            else:
                raise RuntimeError("Circuit is open - call rejected")

        try:
            result = func(*args)
        except Exception:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise

        self.state = "closed"
        return result


def flaky_service(should_fail: bool) -> str:
    if should_fail:
        raise ValueError("Service unavailable")
    return "Service response OK"


if __name__ == "__main__":
    breaker = CircuitBreaker(failure_threshold=2, cooldown_seconds=5.0)
    for attempt in range(4):
        try:
            print(breaker.call(flaky_service, True))
        except Exception as exc:
            print(f"Attempt {attempt}: {exc}")