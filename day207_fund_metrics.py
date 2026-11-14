"""Day 207 - Fund Metrics: DPI, RVPI and TVPI.

All three are multiples of PAID-IN capital (money actually called, not
the commitment): DPI = distributions / paid-in (cash back so far),
RVPI = NAV / paid-in (value still held), TVPI = DPI + RVPI (total
value). A fund that has not called any capital yet has no multiple, so
that case is rejected, not divided by zero - PCPP1 standard.
"""
from __future__ import annotations


def dpi(distributions: float, paid_in: float) -> float:
    """Distributions to paid-in: the realised multiple."""
    if paid_in <= 0:
        raise ValueError("no paid-in capital yet: multiples are undefined")
    return distributions / paid_in


def rvpi(nav: float, paid_in: float) -> float:
    """Residual value to paid-in: the unrealised multiple."""
    if paid_in <= 0:
        raise ValueError("no paid-in capital yet: multiples are undefined")
    return nav / paid_in


def tvpi(distributions: float, nav: float, paid_in: float) -> float:
    """Total value to paid-in: realised plus unrealised."""
    return dpi(distributions, paid_in) + rvpi(nav, paid_in)


def summarise(
    contributions: list[float], distributions: list[float], nav: float, committed: float
) -> dict[str, float]:
    """Headline fund metrics from the call, distribution and NAV history."""
    paid_in = sum(contributions)
    total_distributions = sum(distributions)
    return {
        "paid_in": paid_in,
        "paid_in_pct_of_commitment": paid_in / committed,
        "dpi": dpi(total_distributions, paid_in),
        "rvpi": rvpi(nav, paid_in),
        "tvpi": tvpi(total_distributions, nav, paid_in),
    }


if __name__ == "__main__":
    print(summarise([4_000_000.0, 3_000_000.0, 1_000_000.0], [500_000.0, 1_500_000.0], 7_200_000.0, 10_000_000.0))
    try:
        summarise([], [], 0.0, 10_000_000.0)
    except ValueError as exc:
        print(f"Rejected: {exc}")