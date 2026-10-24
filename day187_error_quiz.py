"""Day 187 - Direct Capitalisation and Net Initial Yield: Error Quiz. Find and fix three bugs."""


def value_from_cap_rate(noi: float, cap_rate: float) -> float:
    return noi / cap_rate


def net_initial_yield(noi: float, price: float, costs_pct: float) -> float:
    return noi / price


def purchase_price_for_yield(noi: float, target_niy: float, costs_pct: float) -> float:
    return noi / target_niy


if __name__ == "__main__":
    print(round(value_from_cap_rate(1_000_000.0, 0.055)))
    print(round(net_initial_yield(1_000_000.0, 18_000_000.0, 0.068), 4))
    print(round(purchase_price_for_yield(1_000_000.0, 0.052, 0.068)))
    print(value_from_cap_rate(1_000_000.0, 0.0))