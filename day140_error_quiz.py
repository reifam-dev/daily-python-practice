"""Day 140 - Blue-Green Deployment: Error Quiz.

Find and fix three bugs. No location hints.
"""
class DeploymentManager:
    def __init__(self):
        self.environments = {"blue": "v1.0", "green": None}
        self.active = "blue"

    def deploy_to_inactive(self, version: str) -> str:
        inactive = "blue" if self.active == "blue" else "green"
        self.environments[inactive] = version
        return inactive

    def health_check(self, environment: str) -> bool:
        return self.environments[environment] is not None

    def switch_traffic(self, target_environment: str) -> None:
        if not self.health_check(target_environment):
            raise RuntimeError(f"Cannot switch: {target_environment} failed health check")
        self.active = target_environment

    def rollback(self) -> None:
        self.active = "blue" if self.active == "blue" else "green"


if __name__ == "__main__":
    manager = DeploymentManager()
    print("Active:", manager.active, manager.environments[manager.active])

    inactive_env = manager.deploy_to_inactive("v2.0")
    print(f"Deployed v2.0 to {inactive_env}")

    manager.switch_traffic(inactive_env)
    print("Active:", manager.active, manager.environments[manager.active])

    manager.rollback()
    print("After rollback, active:", manager.active, manager.environments[manager.active])