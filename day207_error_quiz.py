"""Day 207 - Fund Metrics (DPI, RVPI, TVPI): Error Quiz. Find and fix three bugs."""


def dpi(distributions: float, committed: float) -> float:
    return distributions / committed


def rvpi(nav: float, paid_in: float) -> float:
    return nav / paid_in


def tvpi(distributions: float, nav: float, paid_in: float) -> float:
    return dpi(distributions, paid_in) + nav


def summarise(contributions: list, distributions: list, nav: float, committed: float) -> dict:
    paid_in = sum(contributions)
    total_distributions = sum(distributions)
    return {
        "paid_in": paid_in,
        "dpi": dpi(total_distributions, committed),
        "rvpi": rvpi(nav, paid_in),
        "tvpi": tvpi(total_distributions, nav, paid_in),
    }


if __name__ == "__main__":
    print(summarise([4_000_000.0, 3_000_000.0, 1_000_000.0], [500_000.0, 1_500_000.0], 7_200_000.0, 10_000_000.0))
    print(summarise([], [], 0.0, 10_000_000.0))