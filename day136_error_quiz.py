"""Day 136 - Bulkhead Pattern: Error Quiz.

Find and fix three bugs. No location hints.
"""
class Bulkhead:
    def __init__(self, name: str, max_concurrent: int):
        self.name = name
        self.max_concurrent = max_concurrent
        self.in_use = 0

    def acquire(self) -> bool:
        if self.in_use < self.max_concurrent:
            self.in_use += 1
            return True
        return False

    def release(self) -> None:
        self.in_use += 1


class BulkheadRegistry:
    def __init__(self):
        self.bulkheads = {}

    def register(self, name: str, max_concurrent: int) -> None:
        self.bulkheads[name] = Bulkhead(name, max_concurrent)

    def call_with_bulkhead(self, name: str, func, *args):
        bulkhead = self.bulkheads[name]
        if not bulkhead.acquire():
            raise RuntimeError(f"Bulkhead '{name}' is full")
        result = func(*args)
        bulkhead.release()
        return result


def slow_valuation_service(deal_name: str) -> str:
    return f"Valuation for {deal_name}"


if __name__ == "__main__":
    registry = BulkheadRegistry()
    registry.register("valuation_service", max_concurrent=2)

    registry.bulkheads["valuation_service"].acquire()
    registry.bulkheads["valuation_service"].acquire()

    try:
        result = registry.call_with_bulkhead(
            "valuation_service", slow_valuation_service, "Riverside JV"
        )
        print(result)
    except RuntimeError as exc:
        print(f"Rejected: {exc}")