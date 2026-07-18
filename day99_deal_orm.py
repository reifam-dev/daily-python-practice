"""Day 99 - SQLAlchemy: Deal and Investor ORM.

Demonstrates the SQLAlchemy 2.0 declarative style with typed mapped
columns, a one-to-many relationship, and a session used as a context
manager with an explicit commit - PCPP1 standard.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

load_dotenv()

_DATABASE_URL = os.environ.get("DATABASE_URL")
if not _DATABASE_URL:
    raise ValueError("DATABASE_URL not set - check your .env file")


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


_engine = create_engine(_DATABASE_URL)
Base.metadata.create_all(_engine)


def add_investor_with_deal(name: str, deal_name: str, market_value: float) -> None:
    """Create an investor and an associated deal in a single transaction."""
    with Session(_engine) as session:
        investor = Investor(name=name)
        deal = Deal(name=deal_name, market_value=market_value, investor=investor)
        session.add(investor)
        session.add(deal)
        session.commit()


def get_deals_over(threshold: float) -> list[Deal]:
    """Return all deals with a market value above the given threshold."""
    with Session(_engine) as session:
        statement = select(Deal).where(Deal.market_value > threshold)
        return list(session.execute(statement).scalars().all())


def get_investor_total(investor_name: str) -> float:
    """Return the total market value of all deals for a named investor."""
    with Session(_engine) as session:
        statement = select(Investor).where(Investor.name == investor_name)
        investor = session.execute(statement).scalar_one()
        return sum(deal.market_value for deal in investor.deals)


if __name__ == "__main__":
    add_investor_with_deal("Fund A", "Riverside JV", 12_500_000.0)
    print(get_deals_over(10_000_000.0))
    print(get_investor_total("Fund A"))