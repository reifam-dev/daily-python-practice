"""
Day 74 – FastAPI Endpoints: path params, query params, Pydantic models, HTTP errors.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Run with: uvicorn day74_deals_api:app --reload
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Real Estate Deals API", version="1.0.0")

_deals_db: dict[int, "Deal"] = {}


class Deal(BaseModel):
    """Pydantic model representing a real estate deal."""

    id: int = Field(..., description="Unique deal identifier.")
    sector: str = Field(..., description="Property sector (e.g. Office, Retail).")
    region: str = Field(..., description="Geographic region of the deal.")
    value: float = Field(..., gt=0, description="Deal value in £m.")
    yield_pct: float = Field(..., gt=0, description="Net initial yield in percent.")


class DealSummary(BaseModel):
    """Summary statistics across all deals."""

    total_deals: int
    total_value: float
    mean_yield: float


@app.get("/deals/search", response_model=list[Deal])
def search_deals(
    sector: str = Query(..., description="Sector to filter by."),
    min_value: float = Query(0.0, description="Minimum deal value in £m."),
) -> list[Deal]:
    """Search deals by sector and minimum value.

    Args:
        sector:    Sector string to match exactly.
        min_value: Minimum deal value filter.

    Returns:
        List of matching Deal objects.
    """
    return [
        d for d in _deals_db.values()
        if d.sector == sector and d.value >= min_value
    ]


@app.get("/deals", response_model=list[Deal])
def get_all_deals() -> list[Deal]:
    """Retrieve all deals.

    Returns:
        List of all Deal objects in the database.
    """
    return list(_deals_db.values())


@app.get("/deals/{deal_id}", response_model=Deal)
def get_deal(deal_id: int) -> Deal:
    """Retrieve a single deal by ID.

    Args:
        deal_id: Path parameter identifying the deal.

    Returns:
        Deal object if found.

    Raises:
        HTTPException: 404 if deal does not exist.
    """
    if deal_id not in _deals_db:
        raise HTTPException(status_code=404, detail="Deal not found.")
    return _deals_db[deal_id]


@app.post("/deals", response_model=Deal, status_code=201)
def create_deal(deal: Deal) -> Deal:
    """Create a new deal.

    Args:
        deal: Deal object parsed from request body.

    Returns:
        The created Deal object.

    Raises:
        HTTPException: 409 if deal ID already exists.
    """
    if deal.id in _deals_db:
        raise HTTPException(status_code=409, detail="Deal ID already exists.")
    _deals_db[deal.id] = deal
    return deal


@app.delete("/deals/{deal_id}")
def delete_deal(deal_id: int) -> dict:
    """Delete a deal by ID.

    Args:
        deal_id: Path parameter identifying the deal.

    Returns:
        Dictionary confirming deletion.

    Raises:
        HTTPException: 404 if deal does not exist.
    """
    if deal_id not in _deals_db:
        raise HTTPException(status_code=404, detail="Deal not found.")
    del _deals_db[deal_id]
    return {"deleted": deal_id}


@app.get("/summary", response_model=DealSummary)
def get_summary() -> DealSummary:
    """Retrieve summary statistics across all deals.

    Returns:
        DealSummary with total count, total value, and mean yield.
    """
    deals = list(_deals_db.values())
    if not deals:
        return DealSummary(total_deals=0, total_value=0.0, mean_yield=0.0)
    total_value = sum(d.value for d in deals)
    mean_yield = sum(d.yield_pct for d in deals) / len(deals)
    return DealSummary(total_deals=len(deals), total_value=total_value, mean_yield=mean_yield)