"""Day 132 - Saga Pattern: Investor Onboarding Saga.

Runs a multi-step process (create investor, create deal, send
confirmation) and, if any step fails partway through, compensates by
undoing the steps that already succeeded, in reverse order -
PCPP1 standard.
"""
from __future__ import annotations

_investors: dict[str, dict] = {}
_deals: dict[str, dict] = {}


class SagaFailedError(Exception):
    """Raised when a saga fails and has been fully rolled back."""


def create_investor(name: str) -> str:
    investor_id = f"inv-{len(_investors) + 1}"
    _investors[investor_id] = {"name": name}
    return investor_id


def undo_create_investor(investor_id: str) -> None:
    _investors.pop(investor_id, None)


def create_deal(investor_id: str, deal_name: str) -> str:
    deal_id = f"deal-{len(_deals) + 1}"
    _deals[deal_id] = {"investor_id": investor_id, "deal_name": deal_name}
    return deal_id


def undo_create_deal(deal_id: str) -> None:
    _deals.pop(deal_id, None)


def send_confirmation(deal_id: str) -> None:
    if deal_id == "deal-1":
        raise ConnectionError("Confirmation service unavailable")
    print(f"Confirmation sent for {deal_id}")


def onboard_investor_with_deal(name: str, deal_name: str) -> dict:
    """Run the onboarding saga, rolling back completed steps on failure."""
    completed_steps: list[tuple[str, str]] = []

    try:
        investor_id = create_investor(name)
        completed_steps.append(("investor", investor_id))

        deal_id = create_deal(investor_id, deal_name)
        completed_steps.append(("deal", deal_id))

        send_confirmation(deal_id)

        return {"investor_id": investor_id, "deal_id": deal_id}

    except Exception as exc:
        for step_type, step_id in reversed(completed_steps):
            if step_type == "investor":
                undo_create_investor(step_id)
                print(f"Rolled back investor: {step_id}")
            elif step_type == "deal":
                undo_create_deal(step_id)
                print(f"Rolled back deal: {step_id}")
        raise SagaFailedError(f"Onboarding failed and was rolled back: {exc}") from exc


if __name__ == "__main__":
    try:
        result = onboard_investor_with_deal("Fund A", "Riverside JV")
        print(result)
    except SagaFailedError as exc:
        print(exc)
        print(f"investors remaining: {list(_investors)}")
        print(f"deals remaining: {list(_deals)}")