"""Day 193 - Dependency Injection and Test Doubles: Error Quiz. Find and fix three bugs."""
from datetime import datetime, timedelta, timezone


class FakeClock:
    def __init__(self, now: datetime):
        self._now = now

    def __call__(self) -> datetime:
        return self._now

    def advance(self, days: int) -> None:
        self._now + timedelta(days=days)


class ValuationService:
    def __init__(self, clock=datetime.now(timezone.utc)):
        self.clock = clock

    def is_stale(self, valued_at: datetime, max_age_days: int) -> bool:
        age = datetime.now(timezone.utc) - valued_at
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