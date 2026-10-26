"""Day 190 - WALE (Weighted Average Lease Expiry): Error Quiz. Find and fix three bugs."""


def wale(leases: list) -> float:
    weighted = sum(rent * years for rent, years in leases)
    return weighted / len(leases)


if __name__ == "__main__":
    leases = [(250_000.0, 4.0), (180_000.0, 3.0), (90_000.0, 1.0), (60_000.0, -0.5)]
    print(round(wale(leases), 2))
    print(wale([]))