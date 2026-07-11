"""Day 92 - LangGraph: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, StateGraph

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

llm = ChatAnthropic(model="claude-sonnet-4-6", api_key=api_key)


class DealState(TypedDict):
    deal_name: str
    market_value: float
    risk_score: float
    outcome: str


def fetch_deal(state: DealState) -> dict:
    return {"market_value": 42_000_000.0}


def assess_risk(state: DealState) -> dict:
    risk = state["market_value"] / 1_000_000
    return {"risk": risk}


def route_by_risk(state: DealState) -> str:
    if state["risk_score"] > 30:
        return "recommend"
    return "escalate"


def recommend(state: DealState) -> dict:
    response = llm.invoke(
        f"Write a one-line investment recommendation for {state['deal_name']}."
    )
    return {"outcome": response.content}


def escalate(state: DealState) -> dict:
    return {"outcome": f"{state['deal_name']} escalated for senior review."}


workflow = StateGraph(DealState)
workflow.add_node("fetch_deal", fetch_deal)
workflow.add_node("assess_risk", assess_risk)
workflow.add_node("recommend", recommend)
workflow.add_node("escalate", escalate)

workflow.add_edge("fetch_deal", "assess_risk")
workflow.add_conditional_edges(
    "assess_risk",
    route_by_risk,
    {"recommend": "recommend", "escalate": "escalate"},
)
workflow.add_edge("recommend", END)
workflow.add_edge("escalate", END)

app = workflow.compile()


if __name__ == "__main__":
    result = app.invoke(
        {"deal_name": "Riverside JV", "market_value": 0.0, "risk_score": 0.0, "outcome": ""}
    )
    print(result["outcome"])