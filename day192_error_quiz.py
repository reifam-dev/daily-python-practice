"""Day 192 - CAGR and Compound Growth: Error Quiz. Find and fix three bugs."""


def cagr(start_value: float, end_value: float, years: int) -> float:
    return (end_value / start_value) ** 1 / years - 1


def cagr_from_series(values: list) -> float:
    years = len(values)
    return (values[-1] / values[0]) ** (1 / years) - 1


def project_value(value: float, rate: float, years: int) -> float:
    return value * (1 + rate * years)


if __name__ == "__main__":
    print(round(cagr(100.0, 121.0, 2), 4))
    print(round(cagr_from_series([100.0, 110.0, 121.0]), 4))
    print(round(project_value(100.0, 0.10, 2), 2))