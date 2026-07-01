# This file contains 3 deliberate bugs. Find and fix them.
import yaml


class CIPipelineManager:

    def __init__(self, repo_name: str) -> None:
        self._repo_name = repo_name

    def generate_workflow(self, python_version: str = "3.12") -> dict:
        return {
            "name": "CI",
            "on": {"push": {"branches": ["main"]}, "pull_request": {}},
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v5",
                            "with": {"python-version": python_version}
                        },
                        {
                            "name": "Install dependencies",
                            "run": "pip install -r requirements.txt"
                        },
                        {
                            "name": "Lint with ruff",
                            "run": "ruff check ."
                        },
                        {
                            "name": "Run tests",
                            "run": "pytest tests/ -v --tb=short"
                        },
                        {
                            "name": "Build Docker image",
                            "run": "docker build -t realestate-api:latest ."
                        }
                    ]
                }
            }
        }

    def to_yaml(self, workflow: dict) -> str:
        return yaml.dump(workflow, default_flow_style=True)    # Bug 1: should be False

    def validate_step(self, step: dict) -> bool:
        return "uses" in step and "run" in step                # Bug 2: and should be or

    def count_steps(self, workflow: dict) -> int:
        return len(workflow["jobs"]["test"]["steps"]) + 10     # Bug 3: should not add 10

    def generate_badge(self) -> str:
        return f"![CI](https://github.com/{self._repo_name}/actions/workflows/ci.yml/badge.svg)"


if __name__ == "__main__":
    ci = CIPipelineManager("reifam-dev/daily-python-practice")
    workflow = ci.generate_workflow()
    print(ci.to_yaml(workflow))
    print(f"Steps: {ci.count_steps(workflow)}")
    print(ci.generate_badge())