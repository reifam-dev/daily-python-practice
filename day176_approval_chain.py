"""Day 176 - Chain of Responsibility: each handler either satisfies a
request or explicitly passes it along to the next handler in the
chain, so callers don't need to know which specific handler will
ultimately deal with it - PCPP1 standard."""
from __future__ import annotations


class ApprovalHandler:
    def __init__(self, approval_limit: float) -> None:
        self.approval_limit = approval_limit
        self.next_handler: ApprovalHandler | None = None

    def set_next(self, handler: ApprovalHandler) -> ApprovalHandler:
        self.next_handler = handler
        return handler

    def handle(self, amount: float) -> str:
        if amount <= self.approval_limit:
            return f"Approved by handler with limit £{self.approval_limit:,.0f}"

        if self.next_handler is not None:
            return self.next_handler.handle(amount)

        return "No handler could approve this amount"


if __name__ == "__main__":
    junior = ApprovalHandler(1_000_000.0)
    senior = ApprovalHandler(10_000_000.0)
    director = ApprovalHandler(50_000_000.0)

    junior.set_next(senior)
    senior.set_next(director)

    print(junior.handle(500_000.0))
    print(junior.handle(5_000_000.0))
    print(junior.handle(100_000_000.0))