"""Day 180 - Distribution Waterfall.

Cash flows down a fixed order of tiers. Each tier is paid from what is
LEFT after the tiers above it: (1) return of invested capital, (2) the
preferred return, (3) whatever remains is split between LP and GP by
the promote percentage. Inputs are validated and the result is checked
to add back up to the cash distributed - PCPP1 standard.
"""
from __future__ import annotations


def run_waterfall(
    cash: float, capital: float, pref_due: float, gp_promote_pct: float
) -> dict[str, float]:
    """Distribute cash through return of capital, pref and promote tiers."""
    if cash < 0 or capital < 0 or pref_due < 0:
        raise ValueError("cash, capital and pref_due must be non-negative")
    if not 0.0 <= gp_promote_pct <= 1.0:
        raise ValueError("gp_promote_pct must be between 0 and 1")

    remaining = cash

    capital_return = min(remaining, capital)
    remaining -= capital_return

    pref_paid = min(remaining, pref_due)
    remaining -= pref_paid

    gp_share = remaining * gp_promote_pct
    lp_share = remaining - gp_share

    result = {
        "return_of_capital": capital_return,
        "preferred_return": pref_paid,
        "lp_residual": lp_share,
        "gp_promote": gp_share,
        "lp_total": capital_return + pref_paid + lp_share,
        "gp_total": gp_share,
    }
    assert abs(result["lp_total"] + result["gp_total"] - cash) < 1e-6
    return result


if __name__ == "__main__":
    print(run_waterfall(15_000_000.0, 10_000_000.0, 2_400_000.0, 0.20))
    print(run_waterfall(11_000_000.0, 10_000_000.0, 2_400_000.0, 0.20))