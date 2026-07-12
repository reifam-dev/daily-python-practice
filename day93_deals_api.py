"""Day 93 - FastAPI Advanced: Deals API.

Demonstrates dependency injection with guaranteed resource cleanup,
background tasks, a custom exception handler and nested Pydantic
response models - PCPP1 standard.
"""
from __future__ import annotations

import os
from collections.abc import Generator

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

load_dotenv()

_DATABASE_URL = os.environ.get("DATABASE_URL")
if not _DATABASE_URL:
    raise ValueError("DATABASE_URL not set - check your .env file")


class DealNotFoundError(Exception):
    """Raised when a requested deal does not exist."""

    def __init__(self, deal_id: int) -> None:
        self.deal_id = deal_id
        super().__init__(f"Deal {deal_id} not found")


class InvestorSummary(BaseModel):
    """Nested summary of investor participation in a deal."""

    total_investors: int


class DealResponse(BaseModel):
    """Public response shape for a single deal."""

    id: int
    name: str
    market_value: float
    summary: InvestorSummary


class FakeSession:
    """Stand-in for a real database session."""

    def close(self) -> None:
        print("session closed")


_FAKE_DB: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Riverside JV",
        "market_value": 12_500_000.0,
        "investors": ["Fund A", "Fund B"],
    },
}


def get_db() -> Generator[FakeSession, None, None]:
    """Yield a database session and guarantee it is closed afterwards."""
    db = FakeSession()
    try:
        yield db
    finally:
        db.close()


def log_deal_notified(deal_name: str) -> None:
    """Background task: record that a notification was sent."""
    print(f"Notification queued for: {deal_name}")


router = APIRouter(prefix="/deals", tags=["deals"])


@router.get("/{deal_id}", response_model=DealResponse)
def read_deal(deal_id: int, db: FakeSession = Depends(get_db)) -> dict:
    """Retrieve a single deal by its identifier."""
    deal = _FAKE_DB.get(deal_id)
    if deal is None:
        raise DealNotFoundError(deal_id)
    return {
        "id": deal["id"],
        "name": deal["name"],
        "market_value": deal["market_value"],
        "summary": {"total_investors": len(deal["investors"])},
    }


@router.post("/{deal_id}/notify", status_code=status.HTTP_202_ACCEPTED)
def notify_deal(
    deal_id: int,
    background_tasks: BackgroundTasks,
    db: FakeSession = Depends(get_db),
) -> dict:
    """Queue a background notification for a deal."""
    deal = _FAKE_DB.get(deal_id)
    if deal is None:
        raise DealNotFoundError(deal_id)
    background_tasks.add_task(log_deal_notified, deal["name"])
    return {"status": "notification queued"}


app = FastAPI(title="Deals API")
app.include_router(router)


@app.exception_handler(DealNotFoundError)
def deal_not_found_handler(request: Request, exc: DealNotFoundError) -> JSONResponse:
    """Return a 404 response for any DealNotFoundError."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": f"Deal {exc.deal_id} not found"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)