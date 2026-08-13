"""Day 124 - Health Checks: Liveness vs Readiness: Error Quiz.

Find and fix three bugs. No location hints.
"""
class ServiceHealth:
    def __init__(self):
        self.database_connected = False
        self.cache_warmed = False
        self.startup_complete = False

    def liveness(self) -> dict:
        return {"status": "ok"}

    def readiness(self) -> dict:
        checks = {
            "database": self.database_connected,
            "cache": self.cache_warmed,
        }
        all_ready = all(checks.values)
        return {"status": "ready" if all_ready else "not_ready", "checks": checks}


def simulate_startup(health: ServiceHealth) -> None:
    health.database_connected = True
    print("Database connected")
    health.cache_warmed = True
    print("Cache warmed")


if __name__ == "__main__":
    health = ServiceHealth()

    print("Before startup:")
    print(" liveness:", health.liveness())
    print(" readiness:", health.readiness())

    simulate_startup(health)

    print("\nAfter startup:")
    print(" liveness:", health.liveness())
    print(" readiness:", health.readiness())