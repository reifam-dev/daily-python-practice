"""Day 120 - Backpressure: Error Quiz.

Find and fix three bugs. No location hints.
"""
import time
from collections import deque

MAX_QUEUE_SIZE = 3


class BoundedQueue:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.items = deque()

    def push(self, item) -> bool:
        self.items.append(item)
        return True

    def pop(self):
        if not self.items:
            return None
        return self.items.popleft()

    def size(self) -> int:
        return len(self.items)


def produce_and_consume(queue: BoundedQueue, items: list[str]) -> list[str]:
    rejected = []
    for item in items:
        accepted = queue.push(item)
        if accepted:
            print(f"Accepted: {item} (queue size: {queue.size()})")
        else:
            rejected.append(item)
            print(f"Rejected (queue full): {item}")

        if queue.size() >= MAX_QUEUE_SIZE:
            processed = queue.pop()
            print(f"Processed: {processed}")

    return rejected


if __name__ == "__main__":
    queue = BoundedQueue(max_size=MAX_QUEUE_SIZE)
    items = [f"deal-{i}" for i in range(6)]
    rejected = produce_and_consume(queue, items)
    print(f"Rejected count: {len(rejected)}")