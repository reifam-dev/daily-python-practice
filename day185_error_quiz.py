"""Day 185 - Timezone-Safe Datetimes: Error Quiz. Find and fix three bugs."""
from datetime import datetime, timedelta, timezone


def make_valuation_timestamp(year: int, month: int, day: int) -> datetime:
    return datetime(year, month, day, 12, 0)


def hours_between(start: datetime, end: datetime) -> float:
    return (end - start).seconds / 3600


def is_after_cutoff(ts: datetime, cutoff: datetime) -> bool:
    return ts > cutoff


def now_utc() -> datetime:
    return datetime.utcnow()


if __name__ == "__main__":
    start = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)
    end = start + timedelta(days=1, hours=2)
    print(hours_between(start, end))

    cutoff = datetime(2026, 10, 1, tzinfo=timezone.utc)
    try:
        print(is_after_cutoff(make_valuation_timestamp(2026, 10, 5), cutoff))
    except TypeError as exc:
        print(f"Crashed: {exc}")
    print(now_utc().tzinfo)