"""Day 97 - Async FastAPI: Concurrent Valuation Fetcher.

Fetches multiple deal valuations concurrently from external sources
using an async httpx client and asyncio.gather, with a bounded timeout
and proper async route handling - PCPP1 standard.
"""
from __future__ import annotations

import asyncio
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

_VALUATION_API_KEY = os.environ.get("VALUATION_API_KEY")
if not _VALUATION_API_KEY:
    raise ValueError("VALUATION_API_KEY not set - check your .env file")

_DEAL_SOURCES: list[str] = [
    "https://api.example.com/valuations/riverside-jv",
    "https://api.example.com/valuations/logistics-portfolio",
    "https://api.example.com/valuations/westgate-retail",
]

_REQUEST_TIMEOUT_SECONDS = 5.0
_GATHER_TIMEOUT_SECONDS = 10.0

app = FastAPI(title="Async Deals API")


async def fetch_valuation(client: httpx.AsyncClient, url: str) -> dict:
    """Fetch a single valuation, raising for any non-2xx response."""
    response = await client.get(
        url, headers={"Authorization": f"Bearer {_VALUATION_API_KEY}"}
    )
    response.raise_for_status()
    return response.json()


async def fetch_all_valuations() -> list[dict]:
    """Fetch all deal valuations concurrently."""
    async with httpx.AsyncClient(timeout=_REQUEST_TIMEOUT_SECONDS) as client:
        tasks = [fetch_valuation(client, url) for url in _DEAL_SOURCES]
        return await asyncio.gather(*tasks)


@app.get("/valuations")
async def get_valuations() -> list[dict]:
    """Return all deal valuations, bounded by an overall timeout."""
    try:
        return await asyncio.wait_for(
            fetch_all_valuations(), timeout=_GATHER_TIMEOUT_SECONDS
        )
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504, detail="Valuation sources timed out"
        ) from exc


@app.get("/valuations/{deal_index}")
async def get_single_valuation(deal_index: int) -> dict:
    """Return a single deal valuation by index."""
    if deal_index >= len(_DEAL_SOURCES):
        raise HTTPException(status_code=404, detail="Deal not found")
    async with httpx.AsyncClient(timeout=_REQUEST_TIMEOUT_SECONDS) as client:
        return await fetch_valuation(client, _DEAL_SOURCES[deal_index])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)