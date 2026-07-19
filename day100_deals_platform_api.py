"""Day 100 - Milestone: Deals Platform API.

A deployable FastAPI service backed by PostgreSQL via SQLAlchemy 2.0,
covering investor and deal CRUD plus a portfolio summary endpoint -
PCPP1 standard. Run via Docker Compose (see docker-compose.yml).
"""
from __future__ import annotations

import os
from collections.abc import Generator

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)

load_dotenv()

_DATABASE_URL = os.environ.get("DATABASE_URL")
if not _DATABASE_URL:
    raise ValueError("DATABASE_URL not set - check your .env file")

_engine = create_engine(_DATABASE_URL)
_SessionLocal = sessionmaker(bind=_engine)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


class Investor(Base):
    """An investor that may hold a stake in multiple deals."""

    __tablename__ = "investors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    deals: Mapped[list["Deal"]] = relationship(back_populates="investor")


class Deal(Base):
    """A real estate deal linked to a single investor."""

    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    market_value: Mapped[float]
    investor_id: Mapped[int] = mapped_column(ForeignKey("investors.id"))
    investor: Mapped["Investor"] = relationship(back_populates="deals")


Base.metadata.create_all(_engine)


class InvestorCreate(BaseModel):
    """Request body for creating an investor."""

    name: str


class DealCreate(BaseModel):
    """Request body for creating a deal."""

    name: str
    market_value: float
    investor_id: int


class PortfolioSummary(BaseModel):
    """Response body summarising an investor's portfolio."""

    investor_name: str
    deal_count: int
    total_value: float
    average_deal_value: float


app = FastAPI(title="Deals Platform API")


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and guarantee it is closed afterwards."""
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/investors", status_code=201)
def create_investor(payload: InvestorCreate, db: Session = Depends(get_db)) -> dict:
    """Create a new investor."""
    investor = Investor(name=payload.name)
    db.add(investor)
    db.commit()
    db.refresh(investor)
    return {"id": investor.id, "name": investor.name}


@app.post("/deals", status_code=201)
def create_deal(payload: DealCreate, db: Session = Depends(get_db)) -> dict:
    """Create a new deal linked to an existing investor."""
    investor = db.get(Investor, payload.investor_id)
    if investor is None:
        raise HTTPException(status_code=404, detail="Investor not found")
    deal = Deal(
        name=payload.name,
        market_value=payload.market_value,
        investor_id=payload.investor_id,
    )
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return {"id": deal.id, "name": deal.name}


@app.get("/deals")
def list_deals(db: Session = Depends(get_db)) -> list[dict]:
    """List all deals in the platform."""
    deals = db.execute(select(Deal)).scalars().all()
    return [{"id": d.id, "name": d.name, "market_value": d.market_value} for d in deals]


@app.get("/portfolio/summary/{investor_id}", response_model=PortfolioSummary)
def portfolio_summary(investor_id: int, db: Session = Depends(get_db)) -> PortfolioSummary:
    """Return aggregate portfolio figures for a single investor."""
    investor = db.get(Investor, investor_id)
    if investor is None:
        raise HTTPException(status_code=404, detail="Investor not found")
    deal_count = len(investor.deals)
    total = sum(deal.market_value for deal in investor.deals)
    average = total / deal_count if deal_count else 0.0
    return PortfolioSummary(
        investor_name=investor.name,
        deal_count=deal_count,
        total_value=total,
        average_deal_value=average,
    )


@app.get("/health")
def health_check() -> dict:
    """Basic liveness endpoint for container orchestration."""
    return {"status": "ok"}