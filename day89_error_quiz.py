# This file contains 3 deliberate bugs. Find and fix them.
import asyncio


class PropertyDataFetcher:

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    async def fetch_yield(self, sector: str) -> dict:
        await asyncio.sleep(0.1)
        yields = {"Office": 4.5, "Retail": 5.5, "Industrial": 5.0}
        return {"sector": sector, "yield_pct": yields.get(sector, 5.0)}

    async def fetch_valuation(self, deal_id: int) -> dict:
        await asyncio.sleep(0.1)
        return {"deal_id": deal_id, "value": deal_id * 10.0}

    async def fetch_all_yields(self, sectors: list[str]) -> list[dict]:
        tasks = [self.fetch_yield(s) for s in sectors]
        return await asyncio.gather(tasks)             # Bug 1: should be *tasks (unpack)

    async def fetch_portfolio(self, deal_ids: list[int]) -> list[dict]:
        tasks = [self.fetch_valuation(d) for d in deal_ids]
        results = await asyncio.gather(*tasks)
        return results

    async def fetch_with_timeout(self, sector: str, timeout: float) -> dict | None:
        try:
            return await asyncio.wait_for(self.fetch_yield(sector), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    def run_sync(self, sectors: list[str]) -> list[dict]:
        return asyncio.run(self.fetch_all_yields(sectors))

    def __repr__(self) -> str:
        return f"PropertyDataFetcher(base_url={self._base_url!r})"

    async def fetch_sequential(self, sectors: list[str]) -> list[dict]:
        results = []
        for sector in sectors:
            result = self.fetch_yield(sector)          # Bug 2: missing await
            results.append(result)
        return results

    async def pipeline(self, sectors: list[str]) -> dict:
        yields = await self.fetch_all_yields(sectors)
        total = sum(y["yield_pct"] for y in yields)
        mean = total / len(yields) + len(yields)       # Bug 3: should not add len(yields)
        return {"mean_yield": mean, "count": len(yields)}


if __name__ == "__main__":
    fetcher = PropertyDataFetcher("https://api.example.com")
    sectors = ["Office", "Retail", "Industrial"]
    results = fetcher.run_sync(sectors)
    print(results)