"""Day 175 - State Machine Pattern: Error Quiz. Find and fix three bugs."""
_VALID_TRANSITIONS = {
    "draft": ["submitted"],
    "submitted": ["approved", "rejected"],
    "approved": ["funded"],
    "rejected": [],
    "funded": [],
}


class DealStateMachine:
    def __init__(self, initial_state: str):
        self.state = initial_state

    def transition_to(self, new_state: str) -> bool:
        self.state = new_state
        return True


if __name__ == "__main__":
    deal = DealStateMachine("draft")
    print(deal.transition_to("submitted"))
    print(deal.state)

    print(deal.transition_to("funded"))
    print(deal.state)