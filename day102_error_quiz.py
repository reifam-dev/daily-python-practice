"""Day 102 - Multi-Agent Coordination: Error Quiz.

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


class ReviewState(TypedDict):
    deal_summary: str
    financial_review: str
    legal_review: str
    final_verdict: str


def financial_reviewer(state: ReviewState) -> dict:
    response = llm.invoke(
        f"As a financial analyst, assess this deal in one sentence: {state['deal_summary']}"
    )
    return {"financial_review": response.content}


def legal_reviewer(state: ReviewState) -> dict:
    response = llm.invoke(
        f"As a legal reviewer, assess this deal in one sentence: {state['deal_summary']}"
    )
    return {"legal_review": response.content}


def combine_verdict(state: ReviewState) -> dict:
    verdict = f"Financial: {state['financial_review']}\nLegal: {state['legal_review']}"
    return {"final_verdict": verdict}


workflow = StateGraph(ReviewState)
workflow.add_node("financial_reviewer", financial_reviewer)
workflow.add_node("legal_reviewer", legal_reviewer)
workflow.add_node("combine_verdict", combine_verdict)

workflow.set_entry_point("financial_reviewer")
workflow.add_edge("financial_reviewer", "combine_verdict")
workflow.add_edge("legal_reviewer", "combine_verdict")
workflow.add_edge("combine_verdict", END)

app = workflow.compile()


if __name__ == "__main__":
    result = app.invoke(
        {"deal_summary": "Logistics portfolio, 6.2% yield, 65% LTV.",
         "financial_review": "", "legal_review": "", "final_verdict": ""}
    )
    print(result["final_verdict"])