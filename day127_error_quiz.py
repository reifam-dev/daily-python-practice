"""Day 127 - Chaos Testing: Error Quiz.

Find and fix three bugs. No location hints.
"""
import random


class ChaosMonkey:
    def __init__(self, failure_rate: float, seed: int = None):
        self.failure_rate = failure_rate
        self.random = random.Random(seed)

    def maybe_fail(self, operation_name: str) -> None:
        if self.random.random() < self.failure_rate:
            raise RuntimeError(f"Chaos-injected failure in: {operation_name}")


def fetch_deal_with_chaos(deal_name: str, chaos: ChaosMonkey) -> dict:
    chaos.maybe_fail("fetch_deal")
    return {"deal_name": deal_name, "market_value": 12_500_000.0}


def run_chaos_trial(trials: int, failure_rate: float) -> dict:
    chaos = ChaosMonkey(failure_rate=failure_rate, seed=42)
    successes = 0
    failures = 0

    for _ in range(trials):
        try:
            fetch_deal_with_chaos("Riverside JV", chaos)
            successes += 1
        except RuntimeError:
            failures += 1

    return {"successes": successes, "failures": failures}


if __name__ == "__main__":
    result = run_chaos_trial(trials=100, failure_rate=0.3)
    print(result)
    observed_rate = result["failures"] / result["successes"]
    print(f"Observed failure rate: {observed_rate:.2f}")