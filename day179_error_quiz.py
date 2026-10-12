"""Day 179 - Loan Amortisation: Error Quiz. Find and fix three bugs."""


def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    monthly_rate = annual_rate / 12
    n = years * 12
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -n)


def build_schedule(principal: float, annual_rate: float, years: int) -> list:
    payment = monthly_payment(principal, annual_rate, years)
    balance = principal
    rows = []
    for month in range(1, years * 12):
        interest = balance * annual_rate
        principal_paid = payment - interest
        balance -= principal_paid
        rows.append((month, round(interest, 2), round(principal_paid, 2), round(balance, 2)))
    return rows


if __name__ == "__main__":
    schedule = build_schedule(250_000.0, 0.05, 25)
    print(schedule[0])
    print(schedule[-1])
    print(len(schedule))
    print(len(build_schedule(120_000.0, 0.0, 10)))