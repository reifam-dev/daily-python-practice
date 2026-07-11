"""Day 92 - LangGraph: Deal Analysis Workflow.

A LangGraph state machine that fetches a deal, assesses its risk and
routes to either a recommendation or an escalation node - PCPP1 standard.
"""
from __future__ import annotations

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, StateGraph

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_llm = ChatAnthropic(model="claude-sonnet-4-6", api_key=_api_key)

_RISK_ESCALATION_THRESHOLD = 30.0


class DealState(TypedDict):
    """Shared state passed between LangGraph nodes."""

    deal_name: str
    market_value: float
    risk_score: float
    outcome: str


def fetch_deal(state: DealState) -> dict:
    """Simulate retrieving a deal's market value from a data source."""
    return {"market_value": 42_000_000.0}


def assess_risk(state: DealState) -> dict:
    """Derive a simple risk score from the deal's market value."""
    risk_score = state["market_value"] / 1_000_000
    return {"risk_score": risk_score}


def route_by_risk(state: DealState) -> str:
    """Route to escalation for high-risk deals, recommendation otherwise."""
    if state["risk_score"] > _RISK_ESCALATION_THRESHOLD:
        return "escalate"
    return "recommend"


def recommend(state: DealState) -> dict:
    """Generate an investment recommendation via the LLM."""
    response = _llm.invoke(
        f"Write a one-line investment recommendation for {state['deal_name']}."
    )
    return {"outcome": response.content}


def escalate(state: DealState) -> dict:
    """Flag a high-risk deal for senior review."""
    return {"outcome": f"{state['deal_name']} escalated for senior review."}


def build_workflow() -> StateGraph:
    """Construct and compile the deal analysis graph."""
    workflow = StateGraph(DealState)
    workflow.add_node("fetch_deal", fetch_deal)
    workflow.add_node("assess_risk", assess_risk)
    workflow.add_node("recommend", recommend)
    workflow.add_node("escalate", escalate)

    workflow.set_entry_point("fetch_deal")
    workflow.add_edge("fetch_deal", "assess_risk")
    workflow.add_conditional_edges(
        "assess_risk",
        route_by_risk,
        {"recommend": "recommend", "escalate": "escalate"},
    )
    workflow.add_edge("recommend", END)
    workflow.add_edge("escalate", END)

    return workflow.compile()


if __name__ == "__main__":
    app = build_workflow()
    result = app.invoke(
        {"deal_name": "Riverside JV", "market_value": 0.0, "risk_score": 0.0, "outcome": ""}
    )
    print(result["outcome"])