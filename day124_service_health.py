"""Day 124 - Health Checks: Liveness vs Readiness.

Distinguishes a liveness check (is the process running at all, used by
an orchestrator to decide whether to restart the container) from a
readiness check (has startup fully completed and can this instance
safely receive traffic) - PCPP1 standard.
"""
from __future__ import annotations


class ServiceHealth:
    """Tracks a service's startup state for liveness and readiness checks."""

    def __init__(self) -> None:
        self.database_connected = False
        self.cache_warmed = False

    def liveness(self) -> dict:
        """Return whether the process itself is alive - always true if this runs."""
        return {"status": "ok"}

    def readiness(self) -> dict:
        """Return whether the service has finished startup and can serve traffic."""
        checks = {
            "database": self.database_connected,
            "cache": self.cache_warmed,
        }
        all_ready = all(checks.values())
        return {"status": "ready" if all_ready else "not_ready", "checks": checks}


def simulate_startup(health: ServiceHealth) -> None:
    """Simulate a service completing its startup sequence step by step."""
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