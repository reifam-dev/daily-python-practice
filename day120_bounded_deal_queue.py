"""Day 120 - Backpressure: Bounded Deal Queue.

A queue with a hard capacity limit: once full, new items are rejected
outright (backpressure applied to the producer) rather than growing
unboundedly or silently dropping items, and the caller is told exactly
what was rejected - PCPP1 standard.
"""
from __future__ import annotations

from collections import deque
from typing import TypeVar

_MAX_QUEUE_SIZE = 3

T = TypeVar("T")


class QueueFullError(Exception):
    """Raised when an item is rejected because the queue is at capacity."""


class BoundedQueue:
    """A FIFO queue with a fixed maximum size, applying backpressure when full."""

    def __init__(self, max_size: int) -> None:
        self.max_size = max_size
        self.items: deque = deque()

    def push(self, item: T) -> bool:
        """Add an item if there is capacity; return False if the queue is full."""
        if len(self.items) >= self.max_size:
            return False
        self.items.append(item)
        return True

    def pop(self) -> T | None:
        """Remove and return the oldest item, or None if the queue is empty."""
        if not self.items:
            return None
        return self.items.popleft()

    def size(self) -> int:
        return len(self.items)


def produce_and_consume(queue: BoundedQueue, items: list[str]) -> list[str]:
    """Push items into the queue, processing one whenever it reaches capacity."""
    rejected: list[str] = []
    for item in items:
        accepted = queue.push(item)
        if accepted:
            print(f"Accepted: {item} (queue size: {queue.size()})")
        else:
            rejected.append(item)
            print(f"Rejected (queue full): {item}")
            continue

        if queue.size() >= queue.max_size:
            processed = queue.pop()
            print(f"Processed: {processed}")

    return rejected


if __name__ == "__main__":
    queue = BoundedQueue(max_size=_MAX_QUEUE_SIZE)
    items = [f"deal-{i}" for i in range(6)]
    rejected = produce_and_consume(queue, items)
    print(f"Rejected count: {len(rejected)}")