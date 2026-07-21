"""Day 102 - Multi-Agent Coordination: Parallel Deal Review.

Two independent LangGraph nodes (financial and legal reviewers) run
from the same entry point and both feed into a combining node, which
LangGraph only executes once both parallel branches have completed -
PCPP1 standard.
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


class ReviewState(TypedDict):
    """Shared state passed between all nodes in the review graph."""

    deal_summary: str
    financial_review: str
    legal_review: str
    final_verdict: str


def financial_reviewer(state: ReviewState) -> dict:
    """Produce a one-sentence financial assessment of the deal."""
    response = _llm.invoke(
        f"As a financial analyst, assess this deal in one sentence: {state['deal_summary']}"
    )
    return {"financial_review": response.content[0].text}


def legal_reviewer(state: ReviewState) -> dict:
    """Produce a one-sentence legal assessment of the deal."""
    response = _llm.invoke(
        f"As a legal reviewer, assess this deal in one sentence: {state['deal_summary']}"
    )
    return {"legal_review": response.content[0].text}


def combine_verdict(state: ReviewState) -> dict:
    """Combine both independent reviews into a single verdict."""
    verdict = f"Financial: {state['financial_review']}\nLegal: {state['legal_review']}"
    return {"final_verdict": verdict}


def build_workflow() -> StateGraph:
    """Construct a graph where two reviewers run in parallel before combining."""
    workflow = StateGraph(ReviewState)
    workflow.add_node("financial_reviewer", financial_reviewer)
    workflow.add_node("legal_reviewer", legal_reviewer)
    workflow.add_node("combine_verdict", combine_verdict)

    workflow.set_entry_point("financial_reviewer")
    workflow.set_entry_point("legal_reviewer")
    workflow.add_edge("financial_reviewer", "combine_verdict")
    workflow.add_edge("legal_reviewer", "combine_verdict")
    workflow.add_edge("combine_verdict", END)

    return workflow.compile()


if __name__ == "__main__":
    app = build_workflow()
    result = app.invoke(
        {"deal_summary": "Logistics portfolio, 6.2% yield, 65% LTV.",
         "financial_review": "", "legal_review": "", "final_verdict": ""}
    )
    print(result["final_verdict"])