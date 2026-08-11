"""Day 123 - Feature Flags and Progressive Rollout: Error Quiz.

Find and fix three bugs. No location hints.
"""
import hashlib


class FeatureFlags:
    def __init__(self):
        self.flags = {}

    def set_rollout(self, flag_name: str, percentage: int) -> None:
        self.flags[flag_name] = percentage

    def is_enabled(self, flag_name: str, user_id: str) -> bool:
        percentage = self.flags.get(flag_name)

        bucket = int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 100
        return bucket < percentage


def calculate_deal_score(deal_name: str, use_new_algorithm: bool) -> float:
    if use_new_algorithm:
        return len(deal_name) * 1.5
    return len(deal_name) * 1.0


if __name__ == "__main__":
    flags = FeatureFlags()
    flags.set_rollout("new_scoring_algorithm", 50)

    for user_id in ["user-1", "user-2", "user-3", "user-4"]:
        enabled = flags.is_enabled("new_scoring_algorithm", user_id)
        score = calculate_deal_score("Riverside JV", enabled)
        print(f"{user_id}: enabled={enabled}, score={score}")