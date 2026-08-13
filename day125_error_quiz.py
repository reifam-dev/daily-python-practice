"""Day 125 - Load Shedding: Error Quiz.

Find and fix three bugs. No location hints.
"""
MAX_CONCURRENT_REQUESTS = 3

PRIORITY_ORDER = {"critical": 0, "normal": 1, "low": 2}


class LoadShedder:
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.active_requests = 0

    def accept(self, priority: str) -> bool:
        if self.active_requests > self.max_concurrent:
            if priority == "critical":
                return True
            return False

        self.active_requests += 1
        return True

    def release(self) -> None:
        self.active_requests -= 1


def process_requests(shedder: LoadShedder, requests: list[dict]) -> dict:
    results = {"accepted": 0, "shed": 0}
    for request in requests:
        accepted = shedder.accept(request["priority"])
        if accepted:
            results["accepted"] += 1
        else:
            results["shed"] += 1
    return results


if __name__ == "__main__":
    shedder = LoadShedder(max_concurrent=MAX_CONCURRENT_REQUESTS)
    requests = [
        {"id": 1, "priority": "normal"},
        {"id": 2, "priority": "critical"},
        {"id": 3, "priority": "normal"},
        {"id": 4, "priority": "low"},
        {"id": 5, "priority": "critical"},
    ]
    result = process_requests(shedder, requests)
    print(result)