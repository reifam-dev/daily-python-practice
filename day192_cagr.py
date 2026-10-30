"""Day 192 - CAGR and Compound Growth.

CAGR = (end / start) ** (1 / years) - 1, with the exponent
parenthesised. A series of N values spans N - 1 growth periods, and a
projection compounds ((1 + r) ** years) rather than adding simple
interest - PCPP1 standard.
"""
from __future__ import annotations


def cagr(start_value: float, end_value: float, years: int) -> float:
    """Compound annual growth rate between two values."""
    if start_value <= 0 or end_value <= 0:
        raise ValueError("start and end values must be positive")
    if years <= 0:
        raise ValueError("years must be positive")
    return (end_value / start_value) ** (1 / years) - 1


def cagr_from_series(values: list[float]) -> float:
    """CAGR of an evenly spaced series; N values span N - 1 periods."""
    if len(values) < 2:
        raise ValueError("need at least two values")
    return cagr(values[0], values[-1], len(values) - 1)


def project_value(value: float, rate: float, years: int) -> float:
    """Value after compounding at rate for the given number of years."""
    return value * (1 + rate) ** years


if __name__ == "__main__":
    print(round(cagr(100.0, 121.0, 2), 4))
    print(round(cagr_from_series([100.0, 110.0, 121.0]), 4))
    print(round(project_value(100.0, 0.10, 2), 2))