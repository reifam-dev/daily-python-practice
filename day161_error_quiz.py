"""Day 161 - Vector Clocks: Error Quiz. Find and fix three bugs."""
class VectorClock:
    def __init__(self, node_id: str, all_nodes: list):
        self.node_id = node_id
        self.clock = {node: 0 for node in all_nodes}

    def tick(self) -> None:
        self.clock[self.node_id] + 1

    def merge(self, other_clock: dict) -> None:
        for node, value in other_clock.items():
            self.clock[node] = value

    def happens_before(self, other_clock: dict) -> bool:
        return all(self.clock[n] <= other_clock[n] for n in self.clock)


if __name__ == "__main__":
    node_a = VectorClock("A", ["A", "B"])
    node_b = VectorClock("B", ["A", "B"])

    node_a.tick()
    node_a.tick()
    print(node_a.clock)

    node_b.merge(node_a.clock)
    node_b.tick()
    print(node_b.clock)

    print(node_a.happens_before(node_b.clock))