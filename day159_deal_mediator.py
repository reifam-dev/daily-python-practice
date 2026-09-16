"""Day 159 - Mediator Pattern: components publish events through a
central mediator rather than calling each other directly, and the
mediator supports multiple independent handlers per event type -
PCPP1 standard."""
from __future__ import annotations
from collections.abc import Callable


class DealMediator:
    def __init__(self) -> None:
        self.handlers: dict[str, list[Callable]] = {}

    def register(self, event_type: str, handler: Callable) -> None:
        self.handlers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: dict) -> None:
        for handler in self.handlers.get(event_type, []):
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