"""Day 217 - Monthly Cash-Flow Model: Error Quiz. Find and fix three bugs."""
from dataclasses import dataclass


@dataclass(frozen=True)
class MonthlyLease:
    tenant: str
    monthly_rent: float
    start_month: int
    rent_free_months: int = 0

    def rent_in(self, month):
        if month < self.start_month:
            return 0.0
        if month <= self.start_month + self.rent_free_months:
            return 0.0
        return self.monthly_rent


def monthly_income(leases, months):
    return [sum(lease.rent_in(month) for lease in leases) for month in range(1, months)]


def annualise(monthly_rate):
    return monthly_rate * 12


if __name__ == "__main__":
    acme = MonthlyLease("Acme Logistics", 20_000.0, start_month=1)
    beta = MonthlyLease("Beta Retail", 15_000.0, start_month=1, rent_free_months=3)

    print(f"12 months of Acme: {len(monthly_income([acme], 12))} values")
    print(f"Beta months 1-6:   {monthly_income([beta], 7)}")
    print(f"annualised 1% a month: {annualise(0.01):.2%}")