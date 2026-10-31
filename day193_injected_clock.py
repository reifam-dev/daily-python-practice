"""Day 193 - Dependency Injection and Test Doubles.

The service never reaches out for the time itself: it asks an injected
clock, so a test can hand it a FakeClock it fully controls. The real
clock is chosen INSIDE the constructor (not as a default argument
value, which Python evaluates only once, at import), the injected
clock is the one actually used, and the fake really advances -
PCPP1 standard.
"""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta, timezone


def system_clock() -> datetime:
    """The real clock: the current moment in UTC."""
    return datetime.now(timezone.utc)


class FakeClock:
    """A test double: time stands still until the test moves it."""

    def __init__(self, now: datetime) -> None:
        self._now = now

    def __call__(self) -> datetime:
        return self._now

    def advance(self, days: int) -> None:
        self._now = self._now + timedelta(days=days)


class ValuationService:
    def __init__(self, clock: Callable[[], datetime] | None = None) -> None:
        self.clock = clock if clock is not None else system_clock

    def is_stale(self, valued_at: datetime, max_age_days: int) -> bool:
        """True if the valuation is older than max_age_days, as of the injected clock."""
        age = self.clock() - valued_at
        return age.days > max_age_days


if __name__ == "__main__":
    clock = FakeClock(datetime(2020, 1, 10, tzinfo=timezone.utc))
    service = ValuationService(clock)
    valued_at = datetime(2020, 1, 5, tzinfo=timezone.utc)

    print(service.is_stale(valued_at, max_age_days=30))
    clock.advance(40)
    print(clock())
    print(service.is_stale(valued_at, max_age_days=30))
    print(callable(ValuationService().clock))