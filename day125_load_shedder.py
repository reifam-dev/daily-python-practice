"""Day 125 - Load Shedding: Deal Request Load Shedder.

Rejects incoming requests once at capacity, except critical-priority
requests, which are always accepted - deliberately protecting the
most important work rather than treating all requests equally under
load - PCPP1 standard.
"""
from __future__ import annotations

_MAX_CONCURRENT_REQUESTS = 3
_PRIORITY_ORDER = {"critical": 0, "normal": 1, "low": 2}


class LoadShedder:
    """Caps concurrent request handling, always admitting critical priority."""

    def __init__(self, max_concurrent: int) -> None:
        self.max_concurrent = max_concurrent
        self.active_requests = 0

    def accept(self, priority: str) -> bool:
        """Return whether a request of this priority should be accepted."""
        if self.active_requests >= self.max_concurrent:
            if priority == "critical":
                self.active_requests += 1
                return True
            return False

        self.active_requests += 1
        return True

    def release(self) -> None:
        """Mark one active request as finished, freeing capacity."""
        if self.active_requests > 0:
            self.active_requests -= 1


def process_requests(shedder: LoadShedder, requests: list[dict]) -> dict:
    """Process requests in priority order, tallying accepted vs shed."""
    ordered = sorted(requests, key=lambda r: _PRIORITY_ORDER[r["priority"]])

    results = {"accepted": 0, "shed": 0}
    for request in ordered:
        accepted = shedder.accept(request["priority"])
        if accepted:
            results["accepted"] += 1
        else:
            results["shed"] += 1
    return results


if __name__ == "__main__":
    shedder = LoadShedder(max_concurrent=_MAX_CONCURRENT_REQUESTS)
    requests = [
        {"id": 1, "priority": "normal"},
        {"id": 2, "priority": "critical"},
        {"id": 3, "priority": "normal"},
        {"id": 4, "priority": "low"},
        {"id": 5, "priority": "critical"},
    ]
    result = process_requests(shedder, requests)
    print(result)