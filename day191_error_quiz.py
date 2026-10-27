"""Day 191 - Rent Roll Aggregation: Error Quiz. Find and fix three bugs."""


def rent_by_sector(leases: list) -> dict:
    totals = {}
    for lease in leases:
        totals[lease["sector"]] = lease["annual_rent"]
    return totals


def share_of_total(totals: dict) -> dict:
    return {sector: round(rent / len(totals) * 100, 1) for sector, rent in totals.items()}


if __name__ == "__main__":
    leases = [
        {"tenant": "Acme Logistics", "sector": "logistics", "annual_rent": 250_000.0},
        {"tenant": "Beta Retail", "sector": "retail", "annual_rent": 120_000.0},
        {"tenant": "Gamma Office", "sector": "office", "annual_rent": 180_000.0},
        {"tenant": "Delta Logistics", "sector": "logistics", "annual_rent": 90_000.0},
        {"tenant": "Epsilon Retail", "sector": "retail", "annual_rent": 60_000.0},
    ]
    totals = rent_by_sector(leases)
    print(totals)
    print(share_of_total(totals))