# This file contains 3 deliberate bugs. Find and fix them.
import itertools
from typing import Generator, Iterator


class DealPipeline:

    def __init__(self, deals: list[dict]) -> None:
        self._deals = deals

    def yield_above(self, threshold: float) -> Generator[dict, None, None]:
        for deal in self._deals:
            if deal["yield_pct"] > threshold:
                yield deal

    def running_total(self) -> Generator[float, None, None]:
        total = 0.0
        for deal in self._deals:
            total =+ deal["value"]             # Bug 1: =+ should be +=
            yield total

    def chunked(self, size: int) -> Generator[list[dict], None, None]:
        for i in range(0, len(self._deals), size):
            yield self._deals[i:i + size]

    def top_n_by_value(self, n: int) -> list[dict]:
        return list(itertools.islice(
            sorted(self._deals, key=lambda d: d["value"]),  # Bug 2: missing reverse=True
            n
        ))

    def sector_cycle(self, n: int) -> list[str]:
        sectors = list({d["sector"] for d in self._deals})
        return list(itertools.islice(itertools.cycle(sectors), n))

    def paired_deals(self) -> list[tuple]:
        return list(itertools.combinations(self._deals, 2))

    def flat_tags(self) -> list[str]:
        tags = [d.get("tags", []) for d in self._deals]
        return list(itertools.chain(tags))     # Bug 3: should be itertools.chain.from_iterable(tags)

    def __repr__(self) -> str:
        return f"DealPipeline(deals={len(self._deals)})"


if __name__ == "__main__":
    deals = [
        {"id": 1, "sector": "Office", "value": 80.0, "yield_pct": 4.5, "tags": ["prime", "city"]},
        {"id": 2, "sector": "Retail", "value": 30.0, "yield_pct": 5.5, "tags": ["secondary"]},
        {"id": 3, "sector": "Industrial", "value": 60.0, "yield_pct": 5.0, "tags": ["logistics", "prime"]},
        {"id": 4, "sector": "Office", "value": 50.0, "yield_pct": 4.8, "tags": ["west-end"]},
    ]
    dp = DealPipeline(deals)
    print(repr(dp))
    print("Above 4.7%:", list(dp.yield_above(4.7)))
    print("Running total:", list(dp.running_total()))
    print("Top 2:", dp.top_n_by_value(2))
    print("Flat tags:", dp.flat_tags())