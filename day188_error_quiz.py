"""Day 188 - Sensitivity Grid: Error Quiz. Find and fix three bugs."""


def sensitivity_grid(noi: float, growth_rates: list, cap_rates: list, years: int) -> list:
    grid = [[0.0] * len(cap_rates)] * len(growth_rates)
    for i, growth in enumerate(growth_rates):
        for j, cap_rate in enumerate(cap_rates):
            exit_noi = noi * (1 + growth * years)
            grid[i][j] = round(exit_noi / cap_rate)
    return grid


if __name__ == "__main__":
    grid = sensitivity_grid(1_000_000.0, [0.0, 0.02, 0.04], [0.05, 0.055, 0.06], 5)
    for row in grid:
        print(row)
    print(sensitivity_grid(1_000_000.0, [0.02], [0.0], 5))