"""Day 188 - Two-Way Sensitivity Grid: exit value by NOI growth and exit cap rate.

Each row is built as its own new list (never [[0] * n] * m, which makes
every row the SAME list). NOI grows with COMPOUND interest, and cap
rates are validated before any division - PCPP1 standard.
"""
from __future__ import annotations


def sensitivity_grid(
    noi: float, growth_rates: list[float], cap_rates: list[float], years: int
) -> list[list[int]]:
    """Rows are growth rates, columns are exit cap rates."""
    if any(cap_rate <= 0 for cap_rate in cap_rates):
        raise ValueError("every cap rate must be positive")

    grid: list[list[int]] = []
    for growth in growth_rates:
        exit_noi = noi * (1 + growth) ** years
        grid.append([round(exit_noi / cap_rate) for cap_rate in cap_rates])
    return grid


def format_grid(grid: list[list[int]], growth_rates: list[float], cap_rates: list[float]) -> str:
    """Render the grid as a labelled text table."""
    header = "growth \\ cap  " + "  ".join(f"{c:>10.2%}" for c in cap_rates)
    lines = [header]
    for growth, row in zip(growth_rates, grid):
        lines.append(f"{growth:>12.1%}  " + "  ".join(f"{value:>10,}" for value in row))
    return "\n".join(lines)


if __name__ == "__main__":
    growth_rates = [0.0, 0.02, 0.04]
    cap_rates = [0.05, 0.055, 0.06]
    grid = sensitivity_grid(1_000_000.0, growth_rates, cap_rates, 5)
    print(format_grid(grid, growth_rates, cap_rates))
    try:
        sensitivity_grid(1_000_000.0, [0.02], [0.0], 5)
    except ValueError as exc:
        print(f"Rejected: {exc}")