"""Day 110 - LLM Output Evaluation: Error Quiz.

Find and fix three bugs. No location hints.
"""
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

client = Anthropic(api_key=api_key)

TEST_CASES = [
    {"question": "What is 60% LTV of a 10m property?", "expected_contains": "6m"},
    {"question": "What is 65% LTV of a 20m property?", "expected_contains": "13m"},
]


def generate_answer(question: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


def judge_answer(question: str, answer: str, expected_contains: str) -> bool:
    judge_prompt = (
        f"Question: {question}\nAnswer: {answer}\n"
        f"Does the answer correctly convey the value '{expected_contains}'? "
        "Reply with only YES or NO."
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    verdict = response.content[0].text
    return verdict is "YES"


def run_eval_suite(test_cases: list[dict]) -> float:
    passed = 0
    for case in test_cases:
        answer = generate_answer(case["question"])
        if judge_answer(case["question"], answer, case["expected_contains"]):
            passed =+ 1

    return passed / len(test_cases)


if __name__ == "__main__":
    score = run_eval_suite(TEST_CASES)
    print(f"Pass rate: {score:.0%}")