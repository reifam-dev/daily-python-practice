"""Day 146 - Distributed Locking: Deal Revaluation Lock.

A lock includes both an expiry (TTL) so a crashed holder can't lock a
resource forever, and ownership tracking so only the process that
acquired a lock can release it - preventing worker B from accidentally
releasing a lock still legitimately held by worker A - PCPP1
standard.
"""
from __future__ import annotations

import time

_locks: dict[str, tuple[str, float]] = {}


class LockNotHeldError(Exception):
    """Raised when releasing a lock that isn't held, or held by someone else."""


def acquire_lock(resource_id: str, holder_id: str, ttl_seconds: float) -> bool:
    """Acquire a lock if free or expired; return whether acquisition succeeded."""
    now = time.time()

    if resource_id in _locks:
        _, expires_at = _locks[resource_id]
        if now < expires_at:
            return False

    _locks[resource_id] = (holder_id, now + ttl_seconds)
    return True


def release_lock(resource_id: str, holder_id: str) -> bool:
    """Release a lock, but only if the caller genuinely holds it."""
    if resource_id not in _locks:
        raise LockNotHeldError(f"No lock held on {resource_id}")

    current_holder, _ = _locks[resource_id]
    if current_holder != holder_id:
        raise LockNotHeldError(
            f"{holder_id} does not hold the lock on {resource_id} (held by {current_holder})"
        )

    del _locks[resource_id]
    return True


def process_deal_revaluation(deal_id: str, worker_id: str) -> str:
    """Revalue a deal only if the lock can be acquired, always releasing after."""
    if not acquire_lock(deal_id, worker_id, ttl_seconds=5.0):
        return f"{worker_id}: skipped, {deal_id} is locked"

    try:
        return f"{worker_id}: revalued {deal_id}"
    finally:
        release_lock(deal_id, worker_id)


if __name__ == "__main__":
    print(process_deal_revaluation("deal-1", "worker-a"))
    print(process_deal_revaluation("deal-1", "worker-b"))

    # worker-b trying to release a lock it never held should fail loudly
    acquire_lock("deal-2", "worker-a", ttl_seconds=5.0)
    try:
        release_lock("deal-2", "worker-b")
    except LockNotHeldError as exc:
        print(f"Rejected: {exc}")