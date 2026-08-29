"""Day 141 - Canary Releases: Canary Release Manager.

Routes a small, deterministic percentage of traffic to a "canary"
version, tracks its error rate separately from the stable version,
and only recommends promoting the canary to full traffic if its
observed error rate stays under a configured threshold -
PCPP1 standard.
"""
from __future__ import annotations

import hashlib


class CanaryRelease:
    """Routes traffic between stable and canary, tracking canary health."""

    def __init__(self, canary_percentage: int) -> None:
        if not 0 <= canary_percentage <= 100:
            raise ValueError("canary_percentage must be between 0 and 100")
        self.canary_percentage = canary_percentage
        self.error_count = 0
        self.request_count = 0

    def route_request(self, user_id: str) -> str:
        """Deterministically route a user to canary or stable."""
        bucket = int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 100
        if bucket < self.canary_percentage:
            return "canary"
        return "stable"

    def record_result(self, version: str, succeeded: bool) -> None:
        """Record the outcome of a request, tracked only for the canary version."""
        if version != "canary":
            return
        self.request_count += 1
        if not succeeded:
            self.error_count += 1

    def canary_error_rate(self) -> float:
        """Return the canary's observed error rate, or 0.0 if it has no traffic yet."""
        if self.request_count == 0:
            return 0.0
        return self.error_count / self.request_count

    def should_promote(self, max_error_rate: float) -> bool:
        """Return whether the canary is healthy enough to promote to full traffic."""
        if self.request_count == 0:
            return False
        return self.canary_error_rate() < max_error_rate


if __name__ == "__main__":
    canary = CanaryRelease(canary_percentage=10)

    for i in range(20):
        user_id = f"user-{i}"
        version = canary.route_request(user_id)
        succeeded = not (version == "canary" and i == 3)
        canary.record_result(version, succeeded)

    print(f"Canary requests: {canary.request_count}, errors: {canary.error_count}")
    print(f"Error rate: {canary.canary_error_rate():.2%}")
    print(f"Should promote: {canary.should_promote(max_error_rate=0.05)}")