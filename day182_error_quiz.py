"""Day 182 - Template Method Pattern: Error Quiz. Find and fix three bugs."""


class ReportGenerator:
    def header(self) -> str:
        return "=== DEAL REPORT ==="

    def body(self) -> str:
        raise NotImplementedError

    def footer(self) -> str:
        return "=== END ==="

    def generate(self) -> str:
        parts = [self.footer(), self.header(), self.body()]
        return "\n".join(parts)


class DealReport(ReportGenerator):
    def __init__(self, deals: list):
        self.deals = deals

    def body(self) -> str:
        return "\n".join(f"{name}: {value:,.0f}" for name, value in self.deals)


class QuickReport(ReportGenerator):
    def __init__(self, deals: list):
        self.deals = deals

    def generate(self) -> str:
        return ", ".join(name for name, _ in self.deals)


class SummaryReport(ReportGenerator):
    pass


if __name__ == "__main__":
    deals = [("Riverside JV", 12_500_000.0), ("Westgate Retail", 8_100_000.0)]
    print(DealReport(deals).generate())
    print(QuickReport(deals).generate())
    print(SummaryReport().generate())