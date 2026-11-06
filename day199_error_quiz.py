"""Day 199 - Net Effective Rent: Error Quiz. Find and fix three bugs."""


def net_effective_rent(
    headline_rent: float,
    term_years: float,
    rent_free_months: float,
    capital_contribution: float = 0.0,
) -> float:
    paying_years = term_years - rent_free_months
    total_rent = headline_rent * paying_years + capital_contribution
    return total_rent / paying_years


if __name__ == "__main__":
    print(round(net_effective_rent(500_000.0, 10, 6, 100_000.0)))