"""Day 208 - Rent Review with Cap and Collar.

At review the rent follows an index, limited by a CAP (the most it may
rise) and a COLLAR (the least it must rise; a collar of zero makes the
review upward-only). Index growth is the RATIO end/start (index points
are not percentages), and cap and collar are quoted per year, so over
the review period they COMPOUND: (1 + rate) ** years - PCPP1 standard.
"""
from __future__ import annotations


def reviewed_rent(
    old_rent: float,
    index_start: float,
    index_end: float,
    years: int,
    cap_pa: float = 0.03,
    collar_pa: float = 0.0,
) -> float:
    """The rent after review: index-linked, floored by the collar, capped."""
    if old_rent <= 0 or index_start <= 0 or index_end <= 0:
        raise ValueError("rent and index values must be positive")
    if years <= 0:
        raise ValueError("years must be positive")
    if collar_pa > cap_pa:
        raise ValueError("collar cannot exceed cap")

    index_growth = index_end / index_start
    cap = (1 + cap_pa) ** years
    collar = (1 + collar_pa) ** years
    factor = min(max(index_growth, collar), cap)
    return old_rent * factor


if __name__ == "__main__":
    print(round(reviewed_rent(100_000.0, 120.0, 132.0, 5)))  # inside the band
    print(round(reviewed_rent(100_000.0, 120.0, 114.0, 5)))  # index fell: upward-only
    print(round(reviewed_rent(100_000.0, 120.0, 156.0, 5)))  # above the cap