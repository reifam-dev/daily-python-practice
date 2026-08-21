"""Day 132 - Saga Pattern: Error Quiz.

Find and fix three bugs. No location hints.
"""
_investors = {}
_deals = {}


def create_investor(name: str) -> str:
    investor_id = f"inv-{len(_investors) + 1}"
    _investors[investor_id] = {"name": name}
    return investor_id


def undo_create_investor(investor_id: str) -> None:
    del _investors[investor_id]


def create_deal(investor_id: str, deal_name: str) -> str:
    deal_id = f"deal-{len(_deals) + 1}"
    _deals[deal_id] = {"investor_id": investor_id, "deal_name": deal_name}
    return deal_id


def send_confirmation(deal_id: str) -> None:
    if deal_id == "deal-1":
        raise ConnectionError("Confirmation service unavailable")
    print(f"Confirmation sent for {deal_id}")


def onboard_investor_with_deal(name: str, deal_name: str) -> dict:
    completed_steps = []

    investor_id = create_investor(name)
    completed_steps.append(("investor", investor_id))

    deal_id = create_deal(investor_id, deal_name)
    completed_steps.append(("deal", deal_id))

    send_confirmation(deal_id)

    return {"investor_id": investor_id, "deal_id": deal_id}


if __name__ == "__main__":
    result = onboard_investor_with_deal("Fund A", "Riverside JV")
    print(result)