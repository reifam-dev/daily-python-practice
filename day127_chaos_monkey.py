"""Day 127 - Chaos Testing: Chaos Monkey.

Deliberately injects failures at a configured rate to verify calling
code actually handles them (rather than assuming it does), using a
seeded random generator so trial runs are reproducible - PCPP1
standard.
"""
from __future__ import annotations

import random


class ChaosMonkey:
    """Injects failures at a configured probability, seedable for reproducibility."""

    def __init__(self, failure_rate: float, seed: int | None = None) -> None:
        if not 0.0 <= failure_rate <= 1.0:
            raise ValueError("failure_rate must be between 0.0 and 1.0")
        self.failure_rate = failure_rate
        self._random = random.Random(seed)

    def maybe_fail(self, operation_name: str) -> None:
        """Raise a chaos-injected failure with probability failure_rate."""
        if self._random.random() < self.failure_rate:
            raise RuntimeError(f"Chaos-injected failure in: {operation_name}")


def fetch_deal_with_chaos(deal_name: str, chaos: ChaosMonkey) -> dict:
    """Fetch a deal, subject to chaos-injected failure."""
    chaos.maybe_fail("fetch_deal")
    return {"deal_name": deal_name, "market_value": 12_500_000.0}


def run_chaos_trial(trials: int, failure_rate: float) -> dict:
    """Run repeated trials against a seeded ChaosMonkey and tally the outcome."""
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
    total = result["successes"] + result["failures"]
    observed_rate = result["failures"] / total
    print(f"Observed failure rate: {observed_rate:.2f}")