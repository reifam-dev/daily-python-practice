"""
Day 87 – Generators and itertools: advanced pipelines, lazy evaluation, combinatorics.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

import itertools
from typing import Generator, Iterator


class DealPipeline:
    """Lazy evaluation pipeline for real estate deal data using generators and itertools."""

    def __init__(self, deals: list[dict]) -> None:
        """Initialise with a list of deal dictionaries.

        Args:
            deals: List of deal dicts with keys: id, sector, value, yield_pct, tags.
        """
        self._deals: list[dict] = deals

    def yield_above(self, threshold: float) -> Generator[dict, None, None]:
        """Lazily yield deals with yield_pct above a threshold.

        Args:
            threshold: Minimum yield percentage to include.

        Yields:
            Deal dictionaries exceeding the threshold.
        """
        for deal in self._deals:
            if deal["yield_pct"] > threshold:
                yield deal

    def running_total(self) -> Generator[float, None, None]:
        """Lazily yield a running total of deal values.

        Yields:
            Cumulative total value after each deal.
        """
        total = 0.0
        for deal in self._deals:
            total += deal["value"]
            yield total

    def chunked(self, size: int) -> Generator[list[dict], None, None]:
        """Yield successive chunks of deals of a given size.

        Args:
            size: Number of deals per chunk.

        Yields:
            Lists of deals of length up to size.
        """
        for i in range(0, len(self._deals), size):
            yield self._deals[i:i + size]

    def top_n_by_value(self, n: int) -> list[dict]:
        """Return the top n deals by value using islice on a sorted generator.

        Args:
            n: Number of top deals to return.

        Returns:
            List of the n highest-value deals.
        """
        return list(itertools.islice(
            sorted(self._deals, key=lambda d: d["value"], reverse=True),
            n,
        ))

    def sector_cycle(self, n: int) -> list[str]:
        """Return n sector names cycling through available sectors.

        Args:
            n: Number of items to return.

        Returns:
            List of sector strings cycling infinitely.
        """
        sectors = sorted({d["sector"] for d in self._deals})
        return list(itertools.islice(itertools.cycle(sectors), n))

    def paired_deals(self) -> list[tuple]:
        """Return all unique pairs of deals using combinations.

        Returns:
            List of 2-tuples of deal dictionaries.
        """
        return list(itertools.combinations(self._deals, 2))

    def flat_tags(self) -> list[str]:
        """Flatten all deal tags into a single list using chain.from_iterable.

        Returns:
            Flat list of all tag strings across all deals.
        """
        tags = [d.get("tags", []) for d in self._deals]
        return list(itertools.chain.from_iterable(tags))

    def accumulate_values(self) -> list[float]:
        """Return accumulated deal values using itertools.accumulate.

        Returns:
            List of cumulative sums.
        """
        values = [d["value"] for d in self._deals]
        return list(itertools.accumulate(values))

    def sector_groups(self) -> dict[str, list[dict]]:
        """Group deals by sector using itertools.groupby.

        Returns:
            Dictionary mapping sector name to list of deals.
        """
        sorted_deals = sorted(self._deals, key=lambda d: d["sector"])
        return {
            sector: list(group)
            for sector, group in itertools.groupby(sorted_deals, key=lambda d: d["sector"])
        }

    def __iter__(self) -> Iterator[dict]:
        """Return an iterator over all deals.

        Returns:
            Iterator of deal dictionaries.
        """
        return iter(self._deals)

    def __len__(self) -> int:
        """Return the number of deals in the pipeline.

        Returns:
            Integer count of deals.
        """
        return len(self._deals)

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this pipeline.
        """
        return f"DealPipeline(deals={len(self._deals)})"


if __name__ == "__main__":
    deals: list[dict] = [
        {"id": 1, "sector": "Office", "value": 80.0, "yield_pct": 4.5, "tags": ["prime", "city"]},
        {"id": 2, "sector": "Retail", "value": 30.0, "yield_pct": 5.5, "tags": ["secondary"]},
        {"id": 3, "sector": "Industrial", "value": 60.0, "yield_pct": 5.0, "tags": ["logistics", "prime"]},
        {"id": 4, "sector": "Office", "value": 50.0, "yield_pct": 4.8, "tags": ["west-end"]},
    ]

    dp = DealPipeline(deals)
    print(repr(dp))
    print(f"\nAbove 4.7% yield : {list(dp.yield_above(4.7))}")
    print(f"Running total    : {list(dp.running_total())}")
    print(f"Chunked (2)      : {list(dp.chunked(2))}")
    print(f"Top 2 by value   : {dp.top_n_by_value(2)}")
    print(f"Sector cycle (6) : {dp.sector_cycle(6)}")
    print(f"Flat tags        : {dp.flat_tags()}")
    print(f"Accumulated      : {dp.accumulate_values()}")
    print(f"Sector groups    : {list(dp.sector_groups().keys())}")
    print(f"Paired deals     : {len(dp.paired_deals())} pairs")