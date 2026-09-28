"""Day 171 - Retry with Jitter: plain exponential backoff, capped at
max_delay, then "full jitter" (random between 0 and the capped delay)
so many clients retrying simultaneously after an outage don't all
retry at exactly the same moment and re-overwhelm the recovering
service - PCPP1 standard."""
from __future__ import annotations
import random


def compute_backoff_delay(attempt: int, base_delay: float, max_delay: float) -> float:
    """Exponential backoff, capped so it never grows unbounded."""
    delay = base_delay * (2 ** attempt)
    return min(delay, max_delay)


def compute_backoff_with_jitter(attempt: int, base_delay: float, max_delay: float) -> float:
    """Full jitter: random value between 0 and the capped exponential delay."""
    capped_delay = compute_backoff_delay(attempt, base_delay, max_delay)
    return random.uniform(0, capped_delay)


if __name__ == "__main__":
    for attempt in range(6):
        plain = compute_backoff_delay(attempt, base_delay=1.0, max_delay=30.0)
        jittered = compute_backoff_with_jitter(attempt, base_delay=1.0, max_delay=30.0)
        print(f"attempt {attempt}: plain={plain:.2f}s, jittered={jittered:.2f}s")