"""
Day 81 – GitHub Actions CI/CD: workflow generation, YAML output, badge creation.
Pipeline includes: pytest, ruff linting, and Docker image build.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: pip install pyyaml
"""

import yaml
from dataclasses import dataclass, field


@dataclass
class WorkflowConfig:
    """Configuration for a GitHub Actions CI workflow."""

    repo_name: str
    python_versions: list[str] = field(default_factory=lambda: ["3.12"])
    branches: list[str] = field(default_factory=lambda: ["main"])
    test_command: str = "pytest tests/ -v --tb=short"
    lint_command: str = "ruff check ."
    docker_image: str = "realestate-api"
    include_lint: bool = True
    include_docker: bool = True


class CIPipelineManager:
    """Generates and validates GitHub Actions CI/CD workflow configurations."""

    def __init__(self, config: WorkflowConfig) -> None:
        """Initialise with a WorkflowConfig dataclass.

        Args:
            config: Configuration object for the CI pipeline.
        """
        self._config: WorkflowConfig = config

    def generate_workflow(self) -> dict:
        """Generate a GitHub Actions workflow dictionary.

        Includes pytest, ruff linting, and Docker image build steps.

        Returns:
            Dictionary representing the full workflow YAML structure.
        """
        steps: list[dict] = [
            {"uses": "actions/checkout@v4"},
            {
                "name": "Set up Python",
                "uses": "actions/setup-python@v5",
                "with": {"python-version": self._config.python_versions[0]},
            },
            {
                "name": "Install dependencies",
                "run": "pip install --upgrade pip\npip install -r requirements.txt",
            },
        ]

        if self._config.include_lint:
            steps.append({
                "name": "Lint with ruff",
                "run": self._config.lint_command,
            })

        steps.append({
            "name": "Run tests",
            "run": self._config.test_command,
        })

        if self._config.include_docker:
            steps.append({
                "name": "Build Docker image",
                "run": f"docker build -t {self._config.docker_image}:latest .",
            })

        return {
            "name": "CI",
            "on": {
                "push": {"branches": self._config.branches},
                "pull_request": {},
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": steps,
                }
            },
        }

    def generate_matrix_workflow(self) -> dict:
        """Generate a matrix workflow testing multiple Python versions.

        Returns:
            Workflow dict with a Python version matrix.
        """
        return {
            "name": "CI Matrix",
            "on": {
                "push": {"branches": self._config.branches},
                "pull_request": {},
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {
                        "matrix": {"python-version": self._config.python_versions},
                    },
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {
                            "name": "Set up Python ${{ matrix.python-version }}",
                            "uses": "actions/setup-python@v5",
                            "with": {"python-version": "${{ matrix.python-version }}"},
                        },
                        {"name": "Install", "run": "pip install -r requirements.txt"},
                        {"name": "Lint", "run": self._config.lint_command},
                        {"name": "Test", "run": self._config.test_command},
                    ],
                }
            },
        }

    def to_yaml(self, workflow: dict) -> str:
        """Serialise a workflow dictionary to a readable YAML string.

        Args:
            workflow: Workflow dictionary to serialise.

        Returns:
            Formatted YAML string.
        """
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False)

    def validate_step(self, step: dict) -> bool:
        """Validate that a step contains either 'uses' or 'run'.

        Args:
            step: Step dictionary to validate.

        Returns:
            True if valid, False otherwise.
        """
        return "uses" in step or "run" in step

    def count_steps(self, workflow: dict) -> int:
        """Count the number of steps in the test job.

        Args:
            workflow: Workflow dictionary.

        Returns:
            Number of steps as an integer.
        """
        return len(workflow["jobs"]["test"]["steps"])

    def generate_badge(self) -> str:
        """Generate a GitHub Actions status badge in Markdown.

        Returns:
            Markdown badge string for the CI workflow.
        """
        return (
            f"![CI](https://github.com/{self._config.repo_name}"
            f"/actions/workflows/ci.yml/badge.svg)"
        )

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this manager.
        """
        return (
            f"CIPipelineManager(repo='{self._config.repo_name}', "
            f"branches={self._config.branches})"
        )


if __name__ == "__main__":
    config = WorkflowConfig(
        repo_name="reifam-dev/daily-python-practice",
        python_versions=["3.11", "3.12"],
        branches=["main"],
        docker_image="realestate-api",
        include_lint=True,
        include_docker=True,
    )
    ci = CIPipelineManager(config)

    print("=== Single Version Workflow ===")
    workflow = ci.generate_workflow()
    print(ci.to_yaml(workflow))

    print("=== Matrix Workflow ===")
    matrix = ci.generate_matrix_workflow()
    print(ci.to_yaml(matrix))

    print(f"Steps: {ci.count_steps(workflow)}")
    print(ci.generate_badge())
    print(repr(ci))