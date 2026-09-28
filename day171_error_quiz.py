"""Day 171 - Retry with Jitter: Error Quiz. Find and fix three bugs."""
import random


def compute_backoff_delay(attempt: int, base_delay: float, max_delay: float) -> float:
    delay = base_delay * (2 ** attempt)
    return delay


def compute_backoff_with_jitter(attempt: int, base_delay: float, max_delay: float) -> float:
    delay = compute_backoff_delay(attempt, base_delay, max_delay)
    jitter = random.uniform(0, delay)
    return jitter


if __name__ == "__main__":
    for attempt in range(6):
        plain = compute_backoff_delay(attempt, base_delay=1.0, max_delay=30.0)
        jittered = compute_backoff_with_jitter(attempt, base_delay=1.0, max_delay=30.0)
        print(f"attempt {attempt}: plain={plain:.2f}s, jittered={jittered:.2f}s")