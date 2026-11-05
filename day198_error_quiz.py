"""Day 198 - Residual Land Value: Error Quiz. Find and fix three bugs."""


def residual_land_value(
    gdv: float,
    build_cost: float,
    fees_pct: float,
    contingency_pct: float,
    finance_rate: float,
    build_months: int,
    profit_on_gdv_pct: float,
    land_costs_pct: float,
) -> float:
    costs = build_cost * (1 + fees_pct + contingency_pct)
    finance = costs * finance_rate * (build_months / 12)
    profit = costs * profit_on_gdv_pct
    residual = gdv - costs - finance - profit
    return residual * (1 - land_costs_pct)


if __name__ == "__main__":
    print(round(residual_land_value(30_000_000.0, 15_000_000.0, 0.12, 0.05, 0.07, 18, 0.20, 0.068)))