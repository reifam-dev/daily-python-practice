"""Day 218 - Waterfall with GP Catch-Up.

Day 180's waterfall paid one distribution and had three tiers. A real
waterfall runs period by period and carries state, and it has a fourth
tier between the preferred return and the residual split: the GP
catch-up, where the GP takes most or all of the cash until its share of
the profit distributed so far reaches the carry percentage. Three things
are easy to get wrong. The preferred return accrues on UNRETURNED
capital, so it shrinks as capital comes back. The catch-up target is a
share of TOTAL profit distributed, not of the LP's profit. And once the
catch-up is satisfied the residual splits at the carry rate, not at the
catch-up rate - PCPP1 standard.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class WaterfallTerms:
    """The deal terms, fixed for the life of the fund."""

    committed_capital: float
    pref_rate: float
    carry_pct: float
    catch_up_rate: float = 1.0

    def __post_init__(self) -> None:
        if self.committed_capital <= 0:
            raise ValueError("committed_capital must be positive")
        if not 0.0 <= self.carry_pct < 1.0:
            raise ValueError("carry_pct must be at least 0 and below 1")
        if not 0.0 < self.catch_up_rate <= 1.0:
            raise ValueError("catch_up_rate must be above 0 and at most 1")


@dataclass
class WaterfallState:
    """What the waterfall remembers between distributions."""

    unreturned_capital: float
    accrued_pref: float = 0.0
    lp_profit_paid: float = 0.0
    gp_profit_paid: float = 0.0

    @property
    def profit_paid(self) -> float:
        """Total profit distributed so far, to either party."""
        return self.lp_profit_paid + self.gp_profit_paid


@dataclass
class Distribution:
    """One period's split, tier by tier."""

    period: int
    cash: float
    return_of_capital: float = 0.0
    preferred: float = 0.0
    catch_up: float = 0.0
    lp_residual: float = 0.0
    gp_residual: float = 0.0
    tiers: list[str] = field(default_factory=list)

    @property
    def lp_total(self) -> float:
        return self.return_of_capital + self.preferred + self.lp_residual

    @property
    def gp_total(self) -> float:
        return self.catch_up + self.gp_residual


def catch_up_due(state: WaterfallState, carry_pct: float) -> float:
    """Profit the GP still needs so its share of TOTAL profit reaches the carry.

    Solving gp + x = carry * (profit_paid + x) gives x = (carry * profit - gp)
    over (1 - carry). Measuring against the LP's profit alone overpays the GP.
    """
    shortfall = carry_pct * state.profit_paid - state.gp_profit_paid
    if shortfall <= 0.0:
        return 0.0
    return shortfall / (1.0 - carry_pct)


def distribute(state: WaterfallState, terms: WaterfallTerms, period: int, cash: float) -> Distribution:
    """Run one period's cash down the four tiers, updating the state in place."""
    if cash < 0.0:
        raise ValueError("a distribution cannot be negative")

    state.accrued_pref += state.unreturned_capital * terms.pref_rate
    result = Distribution(period=period, cash=cash)
    remaining = cash

    paid = min(remaining, state.unreturned_capital)
    if paid > 0.0:
        result.return_of_capital = paid
        state.unreturned_capital -= paid
        remaining -= paid
        result.tiers.append("return of capital")

    paid = min(remaining, state.accrued_pref)
    if paid > 0.0:
        result.preferred = paid
        state.accrued_pref -= paid
        state.lp_profit_paid += paid
        remaining -= paid
        result.tiers.append("preferred")

    due = catch_up_due(state, terms.carry_pct)
    paid = min(remaining * terms.catch_up_rate, due)
    if paid > 0.0:
        result.catch_up = paid
        state.gp_profit_paid += paid
        remaining -= paid / terms.catch_up_rate
        result.tiers.append("catch-up")

    if remaining > 0.0:
        result.gp_residual = remaining * terms.carry_pct
        result.lp_residual = remaining - result.gp_residual
        state.gp_profit_paid += result.gp_residual
        state.lp_profit_paid += result.lp_residual
        result.tiers.append("residual split")

    return result


def run_waterfall(terms: WaterfallTerms, distributions: list[float]) -> list[Distribution]:
    """Every period's distribution, in order, sharing one state."""
    state = WaterfallState(unreturned_capital=terms.committed_capital)
    return [
        distribute(state, terms, period, cash)
        for period, cash in enumerate(distributions, start=1)
    ]


if __name__ == "__main__":
    terms = WaterfallTerms(committed_capital=10_000_000.0, pref_rate=0.08, carry_pct=0.20)
    results = run_waterfall(terms, [2_000_000.0, 9_000_000.0, 3_000_000.0, 4_000_000.0])

    for result in results:
        print(
            f"period {result.period}: cash {result.cash:>10,.0f} "
            f"LP {result.lp_total:>10,.0f} GP {result.gp_total:>9,.0f} "
            f"[{', '.join(result.tiers)}]"
        )

    lp = sum(result.lp_total for result in results)
    gp = sum(result.gp_total for result in results)
    print(f"LP total {lp:,.0f}, GP total {gp:,.0f}, sum {lp + gp:,.0f}")

    profit_lp = lp - terms.committed_capital
    print(f"GP share of profit {gp / (gp + profit_lp):.2%}")

    try:
        WaterfallTerms(committed_capital=10_000_000.0, pref_rate=0.08, carry_pct=1.0)
    except ValueError as exc:
        print(f"Rejected: {exc}")