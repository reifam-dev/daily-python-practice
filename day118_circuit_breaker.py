"""Day 118 - Circuit Breaker Pattern: Deal Service Circuit Breaker.

Wraps a potentially-failing call with a circuit breaker: after enough
consecutive failures, further calls are rejected immediately for a
cooldown period rather than repeatedly hitting a known-failing
dependency, then cautiously allows one trial call through - PCPP1
standard.
"""
from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any


class CircuitOpenError(Exception):
    """Raised when a call is rejected because the circuit is open."""


class CircuitBreaker:
    """A simple three-state circuit breaker: closed, open, half-open."""

    def __init__(self, failure_threshold: int, cooldown_seconds: float) -> None:
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.failure_count = 0
        self.state = "closed"
        self.opened_at: float | None = None

    def _should_attempt_reset(self) -> bool:
        """Return whether the cooldown period has elapsed since opening."""
        if self.opened_at is None:
            return False
        return time.time() - self.opened_at > self.cooldown_seconds

    def call(self, func: Callable[..., Any], *args: Any) -> Any:
        """Call func through the breaker, tracking failures and state."""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half_open"
            else:
                raise CircuitOpenError("Circuit is open - call rejected")

        try:
            result = func(*args)
        except Exception:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                self.opened_at = time.time()
            raise

        self.failure_count = 0
        self.state = "closed"
        return result


def flaky_service(should_fail: bool) -> str:
    """Simulate a service call that may fail."""
    if should_fail:
        raise ValueError("Service unavailable")
    return "Service response OK"


if __name__ == "__main__":
    breaker = CircuitBreaker(failure_threshold=2, cooldown_seconds=5.0)
    for attempt in range(4):
        try:
            print(breaker.call(flaky_service, True))
        except Exception as exc:
            print(f"Attempt {attempt}: {exc} (state={breaker.state})")