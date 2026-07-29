"""Day 110 - LLM Output Evaluation: Deal Answer Evaluator.

An LLM-as-judge evaluation harness: generates answers to a fixed set
of test questions, then uses a second model call to judge whether
each answer is correct, reporting an overall pass rate - PCPP1
standard.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not set - check your .env file")

_client = Anthropic(api_key=_api_key)


@dataclass(frozen=True)
class TestCase:
    """A single evaluation test case."""

    question: str
    expected_contains: str


_TEST_CASES: list[TestCase] = [
    TestCase("What is 60% LTV of a 10m property?", "6m"),
    TestCase("What is 65% LTV of a 20m property?", "13m"),
]


def generate_answer(question: str) -> str:
    """Generate an answer to a question using the model under test."""
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


def judge_answer(question: str, answer: str, expected_contains: str) -> bool:
    """Use a separate model call to judge whether an answer is correct."""
    judge_prompt = (
        f"Question: {question}\nAnswer: {answer}\n"
        f"Does the answer correctly convey the value '{expected_contains}'? "
        "Reply with only YES or NO."
    )
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    verdict = response.content[0].text.strip().upper()
    return verdict == "YES"


def run_eval_suite(test_cases: list[TestCase]) -> float:
    """Run every test case and return the overall pass rate."""
    if not test_cases:
        return 0.0

    passed = 0
    for case in test_cases:
        answer = generate_answer(case.question)
        if judge_answer(case.question, answer, case.expected_contains):
            passed += 1

    return passed / len(test_cases)


if __name__ == "__main__":
    score = run_eval_suite(_TEST_CASES)
    print(f"Pass rate: {score:.0%}")