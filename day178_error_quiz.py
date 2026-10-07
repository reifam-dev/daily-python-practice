"""Day 178 - NPV and IRR: Error Quiz. Find and fix three bugs."""


def npv(rate: float, cash_flows: list) -> float:
    total = 0.0
    for t, cash_flow in enumerate(cash_flows):
        total += cash_flow / (1 + rate) ** (t + 1)
    return total


def irr(cash_flows: list, low: float = -0.99, high: float = 1.0) -> float:
    mid = low
    for _ in range(100):
        mid = (low + high) / 2
        if npv(mid, cash_flows) > 0:
            high = mid
        else:
            low = mid
    return mid


if __name__ == "__main__":
    flows = [-1000.0, 300.0, 400.0, 500.0]
    print(round(npv(0.10, flows), 2))
    print(round(irr(flows), 4))
    print(round(irr([100.0, 100.0, 100.0]), 4))