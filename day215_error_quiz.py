"""Day 215 - Package Layout and Absolute Imports: Error Quiz. Find and fix three bugs."""
from dataclasses import dataclass

LAYERS = ("domain", "engine", "api")

__all__ = ("find_cycle")


@dataclass(frozen=True)
class Module:
    name: str
    layer: str
    imports: tuple = ()


def layering_breaches(modules):
    breaches = []
    for module in modules.values():
        for imported in module.imports:
            target = modules.get(imported)
            if target is None:
                continue
            if LAYERS.index(target.layer) >= LAYERS.index(module.layer):
                breaches.append(f"{module.name} imports {target.name}")
    return sorted(breaches)


def find_cycle(modules):
    visited = set()
    stack = []

    def walk(name):
        if name in visited:
            return None
        visited.add(name)
        stack.append(name)
        for imported in modules[name].imports:
            if imported in modules:
                found = walk(imported)
                if found is not None:
                    return found
        stack.pop()
        return None

    for name in sorted(modules):
        found = walk(name)
        if found is not None:
            return found
    return None


if __name__ == "__main__":
    modules = {
        module.name: module
        for module in [
            Module("deal", "domain"),
            Module("money", "domain", ("deal",)),
            Module("waterfall", "engine", ("deal", "money")),
            Module("routes", "api", ("waterfall", "deal")),
        ]
    }
    print(f"exports: {len(__all__)}")
    print(f"breaches: {layering_breaches(modules)}")

    cyclic = {
        module.name: module
        for module in [
            Module("deal", "domain", ("routes",)),
            Module("waterfall", "engine", ("deal",)),
            Module("routes", "api", ("waterfall",)),
        ]
    }
    print(f"cycle: {find_cycle(cyclic)}")