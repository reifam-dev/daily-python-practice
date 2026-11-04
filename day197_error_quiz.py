"""Day 197 - Debt Sizing: Error Quiz. Find and fix three bugs."""


def payment_constant(annual_rate: float, years: int) -> float:
    if annual_rate == 0.0:
        return 1 / years
    monthly_rate = annual_rate / 12
    n = years * 12
    return 12 * monthly_rate / (1 - (1 + monthly_rate) ** -n)


def max_loan(
    noi: float,
    value: float,
    rate: float,
    amort_years: int,
    max_ltv: float = 0.65,
    min_icr: float = 2.0,
    min_dscr: float = 1.25,
) -> dict:
    limits = {
        "ltv": max_ltv * value,
        "icr": noi * min_icr / rate,
        "dscr": noi / min_dscr / rate,
    }
    binding = max(limits, key=limits.get)
    return {"max_loan": limits[binding], "binding": binding, **limits}


if __name__ == "__main__":
    result = max_loan(1_000_000.0, 18_000_000.0, 0.055, 25)
    print({key: round(value) if not isinstance(value, str) else value for key, value in result.items()})