"""Day 199 - Net Effective Rent.

A headline rent hides the incentives that bought it. The tenant pays
nothing during the rent-free period, and any capital contribution the
landlord hands over is money out, so net effective rent =
(headline x PAYING years - contribution) / the WHOLE term. Rent-free is
given in months, so it is converted to years before it is subtracted -
PCPP1 standard.
"""
from __future__ import annotations


def net_effective_rent(
    headline_rent: float,
    term_years: float,
    rent_free_months: float,
    capital_contribution: float = 0.0,
) -> float:
    """Annual net effective rent, averaged over the whole lease term."""
    if term_years <= 0:
        raise ValueError("term_years must be positive")
    term_months = term_years * 12
    if not 0 <= rent_free_months < term_months:
        raise ValueError("rent_free_months must be at least 0 and less than the term")

    paying_years = (term_months - rent_free_months) / 12
    total_received = headline_rent * paying_years - capital_contribution
    return total_received / term_years


def incentive_cost_pct(headline_rent: float, net_effective: float) -> float:
    """How much of the headline rent the incentives give away."""
    return 1 - net_effective / headline_rent


if __name__ == "__main__":
    ner = net_effective_rent(500_000.0, 10, 6, 100_000.0)
    print(round(ner))
    print(f"{incentive_cost_pct(500_000.0, ner):.1%}")