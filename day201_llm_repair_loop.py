"""Day 201 - LLM Output Validate-and-Repair Loop.

Model output is untrusted text: parse it, validate it against a schema,
and on failure send the model the SPECIFIC validation errors and ask
again - up to a fixed number of attempts, then fail loudly rather than
returning a half-valid result. A scripted fake model keeps this offline
and deterministic - PCPP1 standard.
"""
from __future__ import annotations

from collections.abc import Callable

from pydantic import BaseModel, Field, ValidationError


class DealTerms(BaseModel):
    deal_name: str = Field(min_length=1)
    loan_amount: float = Field(gt=0)
    ltv: float = Field(ge=0, le=1)


class ExtractionFailedError(Exception):
    """Raised when the model never produced valid output within the attempt budget."""


class ScriptedModel:
    """A fake model that replays fixed replies and records every prompt it saw."""

    def __init__(self, replies: list[str]) -> None:
        self._replies = list(replies)
        self.prompts: list[str] = []

    def __call__(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self._replies[min(len(self.prompts) - 1, len(self._replies) - 1)]


def summarise_errors(exc: ValidationError) -> str:
    """One readable line per validation problem, naming the field."""
    parts = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"]) or "output"
        parts.append(f"{location}: {error['msg']}")
    return "; ".join(parts)


def extract_with_repair(
    model_call: Callable[[str], str], document: str, max_attempts: int = 3
) -> DealTerms:
    """Ask, validate, and on failure re-ask WITH the errors, up to max_attempts."""
    base_prompt = f"Extract deal_name, loan_amount and ltv (0 to 1) as JSON from:\n{document}"
    prompt = base_prompt
    problems = ""

    for _ in range(max_attempts):
        raw = model_call(prompt)
        try:
            return DealTerms.model_validate_json(raw)
        except ValidationError as exc:
            problems = summarise_errors(exc)
            prompt = (
                f"{base_prompt}\n\nYour previous answer was invalid: {problems}\n"
                "Return corrected JSON only."
            )
    raise ExtractionFailedError(f"no valid output after {max_attempts} attempts: {problems}")


if __name__ == "__main__":
    model = ScriptedModel(
        [
            'Sure! {"deal_name": "Riverside JV"}',
            '{"deal_name": "Riverside JV", "loan_amount": 8500000, "ltv": 65}',
            '{"deal_name": "Riverside JV", "loan_amount": 8500000, "ltv": 0.65}',
        ]
    )
    print(extract_with_repair(model, "Loan Agreement: Riverside JV ..."))
    print("calls:", len(model.prompts))
    print("feedback sent:", len(set(model.prompts)) > 1)

    stubborn = ScriptedModel(['{"deal_name": ""}'])
    try:
        extract_with_repair(stubborn, "Loan Agreement: Riverside JV ...")
    except ExtractionFailedError as exc:
        print(f"Rejected: {exc}")