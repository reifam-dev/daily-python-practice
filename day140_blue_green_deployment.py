"""Day 140 - Blue-Green Deployment: Deployment Manager.

Maintains two identical environments (blue and green). A new version
deploys to whichever is currently inactive, is health-checked, and
traffic is switched to it only if healthy - with the previously-active
environment kept intact so a rollback is an instant switch back,
not a redeploy - PCPP1 standard.
"""
from __future__ import annotations


class DeploymentSwitchError(Exception):
    """Raised when switching traffic to a target environment is not safe."""


class DeploymentManager:
    """Manages traffic switching between two environments, blue and green."""

    def __init__(self) -> None:
        self.environments: dict[str, str | None] = {"blue": "v1.0", "green": None}
        self.active = "blue"
        self.previous: str | None = None

    def _other(self, environment: str) -> str:
        return "green" if environment == "blue" else "blue"

    def deploy_to_inactive(self, version: str) -> str:
        """Deploy a new version to whichever environment is not currently active."""
        inactive = self._other(self.active)
        self.environments[inactive] = version
        return inactive

    def health_check(self, environment: str) -> bool:
        return self.environments[environment] is not None

    def switch_traffic(self, target_environment: str) -> None:
        """Switch active traffic to target_environment, only if it's healthy."""
        if not self.health_check(target_environment):
            raise DeploymentSwitchError(
                f"Cannot switch: {target_environment} failed health check"
            )
        self.previous = self.active
        self.active = target_environment

    def rollback(self) -> None:
        """Switch traffic back to the environment active before the last switch."""
        if self.previous is None:
            raise DeploymentSwitchError("No previous environment to roll back to")
        self.active = self.previous
        self.previous = None


if __name__ == "__main__":
    manager = DeploymentManager()
    print("Active:", manager.active, manager.environments[manager.active])

    inactive_env = manager.deploy_to_inactive("v2.0")
    print(f"Deployed v2.0 to {inactive_env}")

    manager.switch_traffic(inactive_env)
    print("Active:", manager.active, manager.environments[manager.active])

    manager.rollback()
    print("After rollback, active:", manager.active, manager.environments[manager.active])