"""Day 201 - LLM Output Validate-and-Repair Loop: Error Quiz. Find and fix three bugs."""
from pydantic import BaseModel, Field, ValidationError


class DealTerms(BaseModel):
    deal_name: str = Field(min_length=1)
    loan_amount: float = Field(gt=0)
    ltv: float = Field(ge=0, le=1)


class ScriptedModel:
    def __init__(self, replies: list):
        self._replies = list(replies)
        self.prompts = []

    def __call__(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self._replies[min(len(self.prompts) - 1, len(self._replies) - 1)]


def extract_with_repair(model_call, document: str, max_attempts: int = 3):
    prompt = f"Extract deal_name, loan_amount and ltv (0 to 1) as JSON from:\n{document}"
    for _ in range(1, max_attempts):
        raw = model_call(prompt)
        try:
            return DealTerms.model_validate_json(raw)
        except ValidationError:
            continue
    return None


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