"""Day 100 - Milestone: Deals Platform API - Error Quiz.

Find and fix three bugs. No location hints.
"""
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Investor(Base):
    __tablename__ = "investors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    deals: Mapped[list["Deal"]] = relationship(back_populates="investor")


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    market_value: Mapped[float]
    investor_id: Mapped[int] = mapped_column(ForeignKey("investors.id"))
    investor: Mapped["Investor"] = relationship(back_populates="deals")


Base.metadata.create_all(engine)


class InvestorCreate(BaseModel):
    name: str


class DealCreate(BaseModel):
    name: str
    market_value: float
    investor_id: int


class PortfolioSummary(BaseModel):
    investor_name: str
    deal_count: int
    total_value: float


app = FastAPI(title="Deals Platform API")


def get_db():
    db = SessionLocal()
    yield db


@app.post("/investors")
def create_investor(payload: InvestorCreate, db: Session = Depends(get_db)) -> dict:
    investor = Investor(name=payload.name)
    db.add(investor)
    db.commit()
    db.refresh(investor)
    return {"id": investor.id, "name": investor.name}


@app.post("/deals")
def create_deal(payload: DealCreate, db: Session = Depends(get_db)) -> dict:
    deal = Deal(name=payload.name, market_value=payload.market_value)
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return {"id": deal.id, "name": deal.name}


@app.get("/deals")
def list_deals(db: Session = Depends(get_db)) -> list[dict]:
    deals = db.execute(select(Deal)).scalars().all()
    return [{"id": d.id, "name": d.name, "market_value": d.market_value} for d in deals]


@app.get("/portfolio/summary/{investor_id}", response_model=PortfolioSummary)
def portfolio_summary(investor_id: int, db: Session = Depends(get_db)):
    investor = db.get(Investor, investor_id)
    if investor is None:
        raise HTTPException(status_code=404, detail="Investor not found")
    total = sum(deal.market_value for deal in investor.deals)
    average = total / len(investor.deals)
    return PortfolioSummary(
        investor_name=investor.name,
        deal_count=len(investor.deals),
        total_value=total,
    )