"""Day 175 - State Machine Pattern: transitions are only permitted if
they're explicitly listed as valid from the current state, preventing
a deal from skipping stages (e.g. draft straight to funded) or
re-entering a terminal state - PCPP1 standard."""
from __future__ import annotations

_VALID_TRANSITIONS: dict[str, list[str]] = {
    "draft": ["submitted"],
    "submitted": ["approved", "rejected"],
    "approved": ["funded"],
    "rejected": [],
    "funded": [],
}


class InvalidTransitionError(Exception):
    pass


class DealStateMachine:
    def __init__(self, initial_state: str) -> None:
        if initial_state not in _VALID_TRANSITIONS:
            raise ValueError(f"Unknown state: {initial_state}")
        self.state = initial_state

    def transition_to(self, new_state: str) -> bool:
        allowed = _VALID_TRANSITIONS.get(self.state, [])
        if new_state not in allowed:
            raise InvalidTransitionError(
                f"Cannot transition from '{self.state}' to '{new_state}'"
            )
        self.state = new_state
        return True


if __name__ == "__main__":
    deal = DealStateMachine("draft")
    print(deal.transition_to("submitted"))
    print(deal.state)

    try:
        deal.transition_to("funded")
    except InvalidTransitionError as exc:
        print(f"Rejected: {exc}")