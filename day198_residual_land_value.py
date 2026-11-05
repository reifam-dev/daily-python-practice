"""Day 198 - Residual Land Value (development appraisal).

What can a developer pay for the site? Start from the completed value
(GDV) and subtract everything else: construction, fees and contingency,
finance, and the developer's profit. Three details matter: finance
accrues on a build that is drawn down gradually, so on AVERAGE only half
the cost is outstanding; profit is a share of GDV (as the parameter says);
and purchaser's costs sit ON TOP of the land price, so the price is the
residual DIVIDED by (1 + costs) - PCPP1 standard.
"""
from __future__ import annotations


def residual_land_value(
    gdv: float,
    build_cost: float,
    fees_pct: float,
    contingency_pct: float,
    finance_rate: float,
    build_months: int,
    profit_on_gdv_pct: float,
    land_costs_pct: float,
) -> dict[str, float | bool]:
    """Return the land value and the appraisal's workings."""
    if gdv <= 0 or build_cost < 0 or build_months <= 0:
        raise ValueError("gdv and build_months must be positive, build_cost non-negative")

    fees = build_cost * fees_pct
    contingency = build_cost * contingency_pct
    costs = build_cost + fees + contingency
    finance = costs * finance_rate * (build_months / 12) / 2
    profit = gdv * profit_on_gdv_pct
    residual = gdv - costs - finance - profit
    land_value = max(residual, 0.0) / (1 + land_costs_pct)

    return {
        "costs": costs,
        "finance": finance,
        "profit": profit,
        "residual": residual,
        "land_value": land_value,
        "viable": residual > 0,
    }


if __name__ == "__main__":
    result = residual_land_value(30_000_000.0, 15_000_000.0, 0.12, 0.05, 0.07, 18, 0.20, 0.068)
    print({key: round(value) if isinstance(value, float) else value for key, value in result.items()})