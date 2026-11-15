"""Day 208 - Rent Review with Cap and Collar: Error Quiz. Find and fix three bugs."""


def reviewed_rent(
    old_rent: float,
    index_start: float,
    index_end: float,
    years: int,
    cap_pa: float = 0.03,
    collar_pa: float = 0.0,
) -> float:
    index_growth = 1 + (index_end - index_start)
    cap = 1 + cap_pa * years
    factor = min(index_growth, cap)
    return old_rent * factor


if __name__ == "__main__":
    print(round(reviewed_rent(100_000.0, 120.0, 132.0, 5)))
    print(round(reviewed_rent(100_000.0, 120.0, 114.0, 5)))
    print(round(reviewed_rent(100_000.0, 120.0, 156.0, 5)))