"""Day 97 - Async FastAPI: Error Quiz.

Find and fix three bugs. No location hints.
"""
import asyncio
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

VALUATION_API_KEY = os.environ.get("VALUATION_API_KEY")
if not VALUATION_API_KEY:
    raise ValueError("VALUATION_API_KEY not set in .env")

app = FastAPI(title="Async Deals API")

_DEAL_SOURCES = [
    "https://api.example.com/valuations/riverside-jv",
    "https://api.example.com/valuations/logistics-portfolio",
    "https://api.example.com/valuations/westgate-retail",
]


async def fetch_valuation(client: httpx.AsyncClient, url: str) -> dict:
    response = client.get(url, headers={"Authorization": f"Bearer {VALUATION_API_KEY}"})
    response.raise_for_status()
    return response.json()


async def fetch_all_valuations() -> list[dict]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        results = [fetch_valuation(client, url) for url in _DEAL_SOURCES]
        return results


@app.get("/valuations")
def get_valuations() -> list[dict]:
    try:
        return asyncio.wait_for(fetch_all_valuations(), timeout=10.0)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Valuation sources timed out")


@app.get("/valuations/{deal_index}")
async def get_single_valuation(deal_index: int) -> dict:
    if deal_index >= len(_DEAL_SOURCES):
        raise HTTPException(status_code=404, detail="Deal not found")
    async with httpx.AsyncClient(timeout=5.0) as client:
        return await fetch_valuation(client, _DEAL_SOURCES[deal_index])