"""Day 154 - Graph Traversal: topological sort via DFS post-order,
using a "visited" set to avoid revisiting shared dependencies more
than once, and detecting cycles rather than recursing forever -
PCPP1 standard."""
from __future__ import annotations


class CyclicDependencyError(Exception):
    pass


def resolve_order(dependencies: dict) -> list:
    visited = set()
    in_progress = set()
    result = []

    def visit(node):
        if node in visited:
            return
        if node in in_progress:
            raise CyclicDependencyError(f"Cycle detected at: {node}")

        in_progress.add(node)
        for dep in dependencies.get(node, []):
            visit(dep)
        in_progress.discard(node)

        visited.add(node)
        result.append(node)

    for node in dependencies:
        visit(node)

    return result


if __name__ == "__main__":
    deps = {
        "deploy": ["build", "test"],
        "build": ["compile"],
        "test": ["compile"],
        "compile": [],
    }
    print(resolve_order(deps))  # compile appears once, before build/test/deploy