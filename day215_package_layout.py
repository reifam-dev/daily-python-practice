"""Day 215 - Package Layout and Absolute Imports.

A flat folder of two hundred modules has no shape; a package does. Three
rules keep it honest: a src layout, so what the tests import is what gets
installed; absolute imports only, because a relative import inside a
module run directly raises ImportError; and a declared layer order, so no
module may import a layer above its own. This module holds the intended
graph and audits it - a cycle is found with a DFS recursion stack (a plain
visited set walks straight past one), an upward import is a layering
breach, and __all__ is a tuple so the package's exports are a deliberate
list rather than an accident - PCPP1 standard.
"""
from __future__ import annotations

from dataclasses import dataclass, field

LAYERS: tuple[str, ...] = ("domain", "engine", "api")

__all__ = ("LAYERS", "Module", "find_cycle", "layer_rank", "layering_breaches")


@dataclass(frozen=True)
class Module:
    """One module in the package: its name, its layer and what it imports."""

    name: str
    layer: str
    imports: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.layer not in LAYERS:
            raise ValueError(f"unknown layer {self.layer!r}, expected one of {LAYERS}")


def layer_rank(layer: str) -> int:
    """Position of a layer in the dependency order; lower may not import higher."""
    if layer not in LAYERS:
        raise ValueError(f"unknown layer {layer!r}")
    return LAYERS.index(layer)


def layering_breaches(modules: dict[str, Module]) -> list[str]:
    """Imports that reach up a layer, which a src layout cannot catch on its own."""
    breaches = []
    for module in modules.values():
        for imported in module.imports:
            target = modules.get(imported)
            if target is None:
                continue
            if layer_rank(target.layer) > layer_rank(module.layer):
                breaches.append(
                    f"{module.name} ({module.layer}) imports {target.name} ({target.layer})"
                )
    return sorted(breaches)


def find_cycle(modules: dict[str, Module]) -> list[str] | None:
    """First import cycle found, as a path that returns to its start, else None.

    The recursion stack is what makes this work: 'visited' alone only says
    a module has been seen before, never that it is still open above us.
    """
    visited: set[str] = set()
    stack: list[str] = []
    on_stack: set[str] = set()

    def walk(name: str) -> list[str] | None:
        if name in on_stack:
            return stack[stack.index(name):] + [name]
        if name in visited:
            return None
        visited.add(name)
        stack.append(name)
        on_stack.add(name)
        for imported in modules[name].imports:
            if imported in modules:
                found = walk(imported)
                if found is not None:
                    return found
        stack.pop()
        on_stack.remove(name)
        return None

    for name in sorted(modules):
        found = walk(name)
        if found is not None:
            return found
    return None


def _index(modules: list[Module]) -> dict[str, Module]:
    return {module.name: module for module in modules}


if __name__ == "__main__":
    healthy = _index(
        [
            Module("deal", "domain"),
            Module("money", "domain"),
            Module("waterfall", "engine", ("deal", "money")),
            Module("routes", "api", ("waterfall", "deal")),
        ]
    )
    print(f"breaches: {layering_breaches(healthy)}")
    print(f"cycle: {find_cycle(healthy)}")

    broken = _index(
        [
            Module("deal", "domain", ("routes",)),
            Module("waterfall", "engine", ("deal",)),
            Module("routes", "api", ("waterfall",)),
        ]
    )
    print(f"breaches: {layering_breaches(broken)}")
    print(f"cycle: {' -> '.join(find_cycle(broken) or [])}")

    try:
        Module("routes", "transport")
    except ValueError as exc:
        print(f"Rejected: {exc}")