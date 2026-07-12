"""Day 93 - FastAPI Advanced: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os
from collections.abc import Generator

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

app = FastAPI(title="Deals API")

_FAKE_DB: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Riverside JV",
        "market_value": 12_500_000.0,
        "investors": ["Fund A", "Fund B"],
    },
}


class InvestorSummary(BaseModel):
    total_investors: int


class DealResponse(BaseModel):
    id: int
    name: str
    market_value: float
    summary: InvestorSummary


class FakeSession:
    def close(self) -> None:
        print("session closed")


def get_db() -> Generator[FakeSession, None, None]:
    db = FakeSession()
    yield db


def log_deal_notified(deal_name: str) -> None:
    print(f"Notification queued for: {deal_name}")


@app.get("/deals/{deal_id}", response_model=DealResponse)
def read_deal(deal_id: int, db: FakeSession = Depends(get_db)) -> dict:
    deal = _FAKE_DB.get(deal_id)
    if deal is None:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Deal not found")
    return {
        "id": deal["id"],
        "name": deal["name"],
        "market_value": deal["market_value"],
        "summary": {"total_investors": len(deal["investors"])},
    }


@app.post("/deals/{deal_id}/notify", status_code=status.HTTP_202_ACCEPTED)
def notify_deal(
    deal_id: int,
    background_tasks: BackgroundTasks,
    db: FakeSession = Depends(get_db),
) -> dict:
    deal = _FAKE_DB.get(deal_id)
    if deal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    background_tasks.add_task
    return {"status": "notification queued"}