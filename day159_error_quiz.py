"""Day 159 - Mediator Pattern: Error Quiz. Find and fix three bugs."""
class DealMediator:
    def __init__(self):
        self.handlers = {}

    def register(self, event_type: str, handler) -> None:
        self.handlers[event_type] = handler

    def publish(self, event_type: str, payload: dict):
        handler = self.handlers[event_type]
        handler(payload)


def on_deal_created(payload: dict) -> None:
    print(f"Notifying investors about: {payload['deal_name']}")


def on_deal_created_audit(payload: dict) -> None:
    print(f"Audit log: deal created - {payload['deal_name']}")


if __name__ == "__main__":
    mediator = DealMediator()
    mediator.register("deal_created", on_deal_created)
    mediator.register("deal_created", on_deal_created_audit)

    mediator.publish("deal_created", {"deal_name": "Riverside JV"})