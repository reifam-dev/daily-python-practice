"""
Day 89 – asyncio: async/await, asyncio.gather, asyncio.wait_for, event loop.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: Python 3.12+
"""

import asyncio
import time
from typing import Any


class PropertyDataFetcher:
    """
    Asynchronous client for fetching property data concurrently.
    Demonstrates async/await, asyncio.gather, wait_for, and the event loop.
    """

    def __init__(self, base_url: str) -> None:
        """Initialise with the base URL of the property data API.

        Args:
            base_url: Root URL of the API (no trailing slash).
        """
        self._base_url: str = base_url.rstrip("/")

    async def fetch_yield(self, sector: str) -> dict[str, Any]:
        """Simulate an async API call to fetch yield for a sector.

        Args:
            sector: Property sector name.

        Returns:
            Dictionary with sector and yield_pct keys.
        """
        await asyncio.sleep(0.1)
        yields: dict[str, float] = {
            "Office": 4.5,
            "Retail": 5.5,
            "Industrial": 5.0,
        }
        return {"sector": sector, "yield_pct": yields.get(sector, 5.0)}

    async def fetch_valuation(self, deal_id: int) -> dict[str, Any]:
        """Simulate an async API call to fetch valuation for a deal.

        Args:
            deal_id: Unique integer identifier for the deal.

        Returns:
            Dictionary with deal_id and value keys.
        """
        await asyncio.sleep(0.1)
        return {"deal_id": deal_id, "value": deal_id * 10.0}

    async def fetch_all_yields(self, sectors: list[str]) -> list[dict[str, Any]]:
        """Fetch yields for multiple sectors concurrently using asyncio.gather.

        Args:
            sectors: List of sector name strings.

        Returns:
            List of yield dictionaries, one per sector.
        """
        tasks = [self.fetch_yield(s) for s in sectors]
        return await asyncio.gather(*tasks)

    async def fetch_portfolio(self, deal_ids: list[int]) -> list[dict[str, Any]]:
        """Fetch valuations for multiple deals concurrently.

        Args:
            deal_ids: List of deal identifier integers.

        Returns:
            List of valuation dictionaries, one per deal.
        """
        tasks = [self.fetch_valuation(d) for d in deal_ids]
        return list(await asyncio.gather(*tasks))

    async def fetch_with_timeout(
        self, sector: str, timeout: float
    ) -> dict[str, Any] | None:
        """Fetch a yield with a timeout; return None if timeout expires.

        Args:
            sector:  Sector name to fetch.
            timeout: Maximum wait time in seconds.

        Returns:
            Yield dictionary or None if timed out.
        """
        try:
            return await asyncio.wait_for(self.fetch_yield(sector), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    async def fetch_sequential(self, sectors: list[str]) -> list[dict[str, Any]]:
        """Fetch yields sequentially (one at a time) for comparison with gather.

        Args:
            sectors: List of sector name strings.

        Returns:
            List of yield dictionaries fetched one by one.
        """
        results: list[dict[str, Any]] = []
        for sector in sectors:
            result = await self.fetch_yield(sector)
            results.append(result)
        return results

    async def pipeline(self, sectors: list[str]) -> dict[str, Any]:
        """Run a full data pipeline: fetch all yields and compute summary stats.

        Args:
            sectors: List of sector name strings.

        Returns:
            Dictionary with mean_yield and count.
        """
        yields = await self.fetch_all_yields(sectors)
        total = sum(y["yield_pct"] for y in yields)
        mean = total / len(yields)
        return {"mean_yield": round(mean, 4), "count": len(yields)}

    def run_sync(self, sectors: list[str]) -> list[dict[str, Any]]:
        """Run the async fetch_all_yields from a synchronous context.

        Args:
            sectors: List of sector name strings.

        Returns:
            List of yield dictionaries.
        """
        return asyncio.run(self.fetch_all_yields(sectors))

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this fetcher.
        """
        return f"PropertyDataFetcher(base_url={self._base_url!r})"


async def main() -> None:
    """Demonstrate concurrent vs sequential fetch timing."""
    fetcher = PropertyDataFetcher("https://api.example.com")
    sectors = ["Office", "Retail", "Industrial"]
    deal_ids = [1, 2, 3, 4, 5]

    print("=== Concurrent fetch (asyncio.gather) ===")
    start = time.perf_counter()
    yields = await fetcher.fetch_all_yields(sectors)
    elapsed = time.perf_counter() - start
    for y in yields:
        print(f"  {y['sector']}: {y['yield_pct']}%")
    print(f"  Time: {elapsed:.3f}s\n")

    print("=== Sequential fetch ===")
    start = time.perf_counter()
    sequential = await fetcher.fetch_sequential(sectors)
    elapsed = time.perf_counter() - start
    print(f"  Results: {sequential}")
    print(f"  Time: {elapsed:.3f}s\n")

    print("=== Portfolio valuations ===")
    valuations = await fetcher.fetch_portfolio(deal_ids)
    for v in valuations:
        print(f"  Deal {v['deal_id']}: £{v['value']}m")

    print("\n=== Timeout test ===")
    result = await fetcher.fetch_with_timeout("Office", timeout=0.05)
    print(f"  Timeout 0.05s: {result}")
    result = await fetcher.fetch_with_timeout("Office", timeout=0.5)
    print(f"  Timeout 0.5s: {result}")

    print("\n=== Pipeline ===")
    summary = await fetcher.pipeline(sectors)
    print(f"  {summary}")

    print(f"\n{repr(fetcher)}")


if __name__ == "__main__":
    asyncio.run(main())