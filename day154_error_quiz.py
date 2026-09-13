"""Day 154 - Graph Traversal: Error Quiz. Find and fix three bugs."""
def resolve_order(dependencies: dict) -> list:
    visited = []
    result = []

    def visit(node):
        visited.append(node)
        for dep in dependencies.get(node, []):
            visit(dep)
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
    print(resolve_order(deps))