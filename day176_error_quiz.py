"""Day 176 - Chain of Responsibility: Error Quiz. Find and fix three bugs."""
class ApprovalHandler:
    def __init__(self, approval_limit: float):
        self.approval_limit = approval_limit
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler

    def handle(self, amount: float) -> str:
        if amount <= self.approval_limit:
            return f"Approved by handler with limit £{self.approval_limit:,.0f}"
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