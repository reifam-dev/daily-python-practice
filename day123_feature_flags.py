"""Day 123 - Feature Flags and Progressive Rollout: Deal Feature Flags.

Enables a feature for a deterministic percentage of users, using a
stable hash of the user id so the same user always gets the same
result on repeat calls, and defaults safely to disabled for any
unregistered flag - PCPP1 standard.
"""
from __future__ import annotations

import hashlib


class FeatureFlags:
    """Percentage-based feature rollout, deterministic per user."""

    def __init__(self) -> None:
        self.flags: dict[str, int] = {}

    def set_rollout(self, flag_name: str, percentage: int) -> None:
        """Register a flag with the percentage of users it should be enabled for."""
        if not 0 <= percentage <= 100:
            raise ValueError("percentage must be between 0 and 100")
        self.flags[flag_name] = percentage

    def is_enabled(self, flag_name: str, user_id: str) -> bool:
        """Return whether the flag is enabled for this specific user."""
        percentage = self.flags.get(flag_name, 0)

        bucket = int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 100
        return bucket < percentage


def calculate_deal_score(deal_name: str, use_new_algorithm: bool) -> float:
    """Score a deal, optionally using the new (flagged) scoring algorithm."""
    if use_new_algorithm:
        return len(deal_name) * 1.5
    return len(deal_name) * 1.0


if __name__ == "__main__":
    flags = FeatureFlags()
    flags.set_rollout("new_scoring_algorithm", 50)

    for user_id in ["user-1", "user-2", "user-3", "user-4"]:
        enabled = flags.is_enabled("new_scoring_algorithm", user_id)
        # calling twice proves determinism - same user, same result
        enabled_again = flags.is_enabled("new_scoring_algorithm", user_id)
        assert enabled == enabled_again, "flag result must be deterministic per user"

        score = calculate_deal_score("Riverside JV", enabled)
        print(f"{user_id}: enabled={enabled}, score={score}")

    print(f"unregistered flag defaults to: {flags.is_enabled('unknown_flag', 'user-1')}")