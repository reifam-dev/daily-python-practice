"""Day 180 - Distribution Waterfall: Error Quiz. Find and fix three bugs."""


def run_waterfall(cash: float, capital: float, pref_due: float, gp_promote_pct: float) -> dict:
    remaining = cash

    capital_return = min(remaining, capital)

    pref_paid = min(remaining, pref_due)
    remaining -= pref_paid

    gp_share = cash * gp_promote_pct
    lp_share = remaining - gp_share

    return {
        "lp_total": capital_return + pref_paid + lp_share,
        "gp_total": gp_share,
    }


if __name__ == "__main__":
    result = run_waterfall(15_000_000.0, 10_000_000.0, 2_400_000.0, 0.20)
    print(result)
    print(result["lp_total"] + result["gp_total"])