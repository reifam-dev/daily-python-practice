"""Day 99 - SQLAlchemy: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")


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


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)


def add_investor_with_deal(name: str, deal_name: str, market_value: float) -> None:
    session = Session(engine)
    investor = Investor(name=name)
    deal = Deal(name=deal_name, market_value=market_value, investor=investor)
    session.add(investor)
    session.add(deal)


def get_deals_over(threshold: float) -> list[Deal]:
    with Session(engine) as session:
        statement = select(Deal).where(Deal.market_value = threshold)
        return session.execute(statement).scalars().all()


def get_investor_total(investor_name: str) -> float:
    with Session(engine) as session:
        statement = select(Investor).where(Investor.name == investor_name)
        investor = session.execute(statement).scalar_one()
        return sum(deal.market_value for deal in investor.deals)


if __name__ == "__main__":
    add_investor_with_deal("Fund A", "Riverside JV", 12_500_000.0)
    print(get_deals_over(10_000_000.0))
    print(get_investor_total("Fund A"))