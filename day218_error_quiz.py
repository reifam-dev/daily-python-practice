"""Day 218 - Waterfall with GP Catch-Up: Error Quiz. Find and fix three bugs."""
from dataclasses import dataclass


@dataclass(frozen=True)
class WaterfallTerms:
    committed_capital: float
    pref_rate: float
    carry_pct: float


@dataclass
class WaterfallState:
    unreturned_capital: float
    accrued_pref: float = 0.0
    lp_profit_paid: float = 0.0
    gp_profit_paid: float = 0.0

    @property
    def profit_paid(self):
        return self.lp_profit_paid + self.gp_profit_paid


def accrue_pref(state, terms):
    state.accrued_pref += terms.committed_capital * terms.pref_rate
    return state.accrued_pref


def catch_up_due(state, carry_pct):
    shortfall = carry_pct * state.lp_profit_paid - state.gp_profit_paid
    if shortfall <= 0.0:
        return 0.0
    return shortfall / (1.0 - carry_pct)


def residual_split(remaining, carry_pct):
    gp = remaining * (1.0 - carry_pct)
    return remaining - gp, gp


if __name__ == "__main__":
    terms = WaterfallTerms(committed_capital=10_000_000.0, pref_rate=0.08, carry_pct=0.20)

    part_returned = WaterfallState(unreturned_capital=6_000_000.0)
    print(f"pref accrued on 6m unreturned: {accrue_pref(part_returned, terms):,.0f}")

    mid_catch_up = WaterfallState(
        unreturned_capital=0.0, lp_profit_paid=800_000.0, gp_profit_paid=100_000.0
    )
    print(f"catch-up still due: {catch_up_due(mid_catch_up, terms.carry_pct):,.0f}")

    lp, gp = residual_split(1_000_000.0, terms.carry_pct)
    print(f"residual split of 1m: LP {lp:,.0f} / GP {gp:,.0f}")