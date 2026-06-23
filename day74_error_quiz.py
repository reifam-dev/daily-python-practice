# This file contains 3 deliberate bugs. Find and fix them.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Deal(BaseModel):
    id: int
    sector: str
    value: float
    yield_pct: float


deals_db: dict[int, Deal] = {}


@app.get("/deals")
def get_all_deals() -> list[Deal]:
    return list(deals_db.values())


@app.get("/deals/{deal_id}")
def get_deal(deal_id: int) -> Deal:
    if deal_id not in deals_db:
        raise HTTPException(status_code=404, details="Deal not found")  # Bug 1
    return deals_db[deal_id]


@app.post("/deals")
def create_deal(deal: Deal) -> Deal:
    deals_db[deal.id] = deal
    return deal


@app.delete("/deals/{deal_id}")
def delete_deal(deal_id: int) -> dict:
    if deal_id not in deals_db:
        raise HTTPException(status_code=404, detail="Deal not found")
    del deals_db[deal_id]
    return {"deleted": deal_id}


@app.get("/deals/search")
def search_deals(sector: str, min_value: float = 0.0) -> list[Deal]:  # Bug 2
    return [d for d in deals_db.values() if d.sector == sector and d.value >= min_value]


class DealSummary(BaseModel):
    total_deals: int
    total_value: float
    mean_yield: float


@app.get("/summary")
def get_summary() -> DealSummary:
    deals = list(deals_db.values())
    if not deals:
        return DealSummary(total_deals=0, total_value=0.0, mean_yield=0.0)
    total_value = sum(d.value for d in deals)
    mean_yield = sum(d.yield_pct for d in deals) + len(deals)  # Bug 3
    return DealSummary(total_deals=len(deals), total_value=total_value, mean_yield=mean_yield)