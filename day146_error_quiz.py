"""Day 146 - Distributed Locking: Error Quiz.

Find and fix three bugs. No location hints.
"""
import time

_locks = {}


def acquire_lock(resource_id: str, holder_id: str, ttl_seconds: float) -> bool:
    now = time.time()

    if resource_id in _locks:
        holder, expires_at = _locks[resource_id]
        if now < expires_at:
            return False

    _locks[resource_id] = (holder_id, now + ttl_seconds)
    return True


def release_lock(resource_id: str, holder_id: str) -> bool:
    del _locks[resource_id]
    return True


def process_deal_revaluation(deal_id: str, worker_id: str) -> str:
    if not acquire_lock(deal_id, worker_id, ttl_seconds=5.0):
        return f"{worker_id}: skipped, {deal_id} is locked"

    result = f"{worker_id}: revalued {deal_id}"
    release_lock(deal_id, worker_id)
    return result


if __name__ == "__main__":
    print(process_deal_revaluation("deal-1", "worker-a"))
    print(process_deal_revaluation("deal-1", "worker-b"))