"""Day 185 - Timezone-Safe Datetimes.

Store and compare moments as timezone-AWARE UTC datetimes. Naive and
aware datetimes cannot be compared, utcnow() returns a naive value (and
is deprecated), and timedelta.seconds is only the leftover seconds
part - total_seconds() is the real duration - PCPP1 standard.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone


def make_valuation_timestamp(year: int, month: int, day: int) -> datetime:
    """A midday valuation moment, explicitly in UTC."""
    return datetime(year, month, day, 12, 0, tzinfo=timezone.utc)


def hours_between(start: datetime, end: datetime) -> float:
    """Elapsed hours, including whole days."""
    return (end - start).total_seconds() / 3600


def is_after_cutoff(ts: datetime, cutoff: datetime) -> bool:
    """Compare two moments, refusing naive datetimes outright."""
    if ts.tzinfo is None or cutoff.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    return ts > cutoff


def now_utc() -> datetime:
    """The current moment as an aware UTC datetime."""
    return datetime.now(timezone.utc)


def to_offset(ts: datetime, hours: int) -> datetime:
    """Show an aware moment at a fixed UTC offset (display only)."""
    return ts.astimezone(timezone(timedelta(hours=hours)))


if __name__ == "__main__":
    start = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)
    end = start + timedelta(days=1, hours=2)
    print(hours_between(start, end))

    cutoff = datetime(2026, 10, 1, tzinfo=timezone.utc)
    print(is_after_cutoff(make_valuation_timestamp(2026, 10, 5), cutoff))
    print(now_utc().tzinfo)
    print(to_offset(make_valuation_timestamp(2026, 10, 5), 1))