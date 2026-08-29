"""Day 141 - Canary Releases: Error Quiz.

Find and fix three bugs. No location hints.
"""
import hashlib


class CanaryRelease:
    def __init__(self, canary_percentage: int):
        self.canary_percentage = canary_percentage
        self.error_count = 0
        self.request_count = 0

    def route_request(self, user_id: str) -> str:
        bucket = int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 100
        if bucket < self.canary_percentage:
            return "canary"
        return "stable"

    def record_result(self, version: str, succeeded: bool) -> None:
        if version == "canary":
            self.request_count += 1
            if not succeeded:
                self.error_count += 1

    def canary_error_rate(self) -> float:
        return self.error_count / self.request_count

    def should_promote(self, max_error_rate: float) -> bool:
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