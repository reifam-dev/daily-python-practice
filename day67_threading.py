# Day 67 - Clean threading module examples
# New concepts: Thread, Lock, Event, daemon threads, thread safety
# PEP 8, docstrings, type hints, exceptions throughout

import threading
import time
from typing import List


class ThreadSafeCounter:
    """A thread-safe counter using a Lock.

    Without the lock, concurrent increments cause race conditions —
    two threads read the same value and both write back +1 when
    the result should be +2.
    """

    def __init__(self) -> None:
        self._value: int = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        """Increment the counter safely."""
        with self._lock:
            self._value += 1

    @property
    def value(self) -> int:
        """Return the current counter value."""
        return self._value


class WorkerPool:
    """Manages a pool of worker threads with a stop event."""

    def __init__(self, num_workers: int) -> None:
        self._num_workers = num_workers
        self._stop_event = threading.Event()
        self._threads: List[threading.Thread] = []
        self._results: List[str] = []
        self._lock = threading.Lock()

    def _worker(self, worker_id: int) -> None:
        """Worker function — runs until stop event is set."""
        with self._lock:
            self._results.append(f"Worker {worker_id} started")
        count = 0
        while not self._stop_event.is_set():
            time.sleep(0.05)
            count += 1
        with self._lock:
            self._results.append(f"Worker {worker_id} completed {count} cycles")

    def start(self) -> None:
        """Start all worker threads."""
        for i in range(self._num_workers):
            t = threading.Thread(target=self._worker, args=(i,), daemon=True)
            self._threads.append(t)
            t.start()

    def stop(self) -> None:
        """Signal all workers to stop and wait for them."""
        self._stop_event.set()
        for t in self._threads:
            t.join(timeout=2)

    def get_results(self) -> List[str]:
        """Return a copy of the results log."""
        return self._results.copy()


if __name__ == "__main__":
    print("=== ThreadSafeCounter ===\n")
    counter = ThreadSafeCounter()
    threads = [
        threading.Thread(target=lambda: [counter.increment() for _ in range(1000)])
        for _ in range(5)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("  Expected : 5000")
    print(f"  Got      : {counter.value}\n")

    print("=== WorkerPool with Event ===\n")
    pool = WorkerPool(3)
    pool.start()
    time.sleep(0.3)
    pool.stop()
    for result in pool.get_results():
        print(f"  {result}")

    print("\n=== threading.Event directly ===\n")
    event = threading.Event()

    def waiter(name: str, ev: threading.Event) -> None:
        print(f"  {name} waiting...")
        ev.wait()
        print(f"  {name} unblocked!")

    t1 = threading.Thread(target=waiter, args=("Thread-A", event))
    t2 = threading.Thread(target=waiter, args=("Thread-B", event))
    t1.start()
    t2.start()
    time.sleep(0.1)
    print("  Setting event...")
    event.set()
    t1.join()
    t2.join()