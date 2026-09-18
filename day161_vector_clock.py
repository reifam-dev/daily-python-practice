"""Day 161 - Vector Clocks: each node tracks its own logical time plus
what it last knew of every other node's time. merge() takes the max
per node (never regresses), and happens_before() correctly detects
causal ordering across nodes - PCPP1 standard."""
from __future__ import annotations


class VectorClock:
    def __init__(self, node_id: str, all_nodes: list[str]) -> None:
        self.node_id = node_id
        self.clock = {node: 0 for node in all_nodes}

    def tick(self) -> None:
        self.clock[self.node_id] += 1

    def merge(self, other_clock: dict[str, int]) -> None:
        for node, value in other_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), value)

    def happens_before(self, other_clock: dict[str, int]) -> bool:
        at_least_as_early = all(self.clock[n] <= other_clock.get(n, 0) for n in self.clock)
        strictly_earlier = any(self.clock[n] < other_clock.get(n, 0) for n in self.clock)
        return at_least_as_early and strictly_earlier


if __name__ == "__main__":
    node_a = VectorClock("A", ["A", "B"])
    node_b = VectorClock("B", ["A", "B"])

    node_a.tick()
    node_a.tick()
    print(node_a.clock)  # {'A': 2, 'B': 0}

    node_b.merge(node_a.clock)
    node_b.tick()
    print(node_b.clock)  # {'A': 2, 'B': 1}

    print(node_a.happens_before(node_b.clock))  # True