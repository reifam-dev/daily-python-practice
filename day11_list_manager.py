# Day 11 - Clean ListManager class (PEP 8, docstrings, type hints, exceptions)

from typing import List, Any

class ListManager:
    """Simple list manager with basic operations."""

    def __init__(self):
        self._items: List[Any] = []

    def add_item(self, item: Any) -> None:
        """Add an item to the list."""
        self._items.append(item)

    def remove_item(self, item: Any) -> bool:
        """Remove an item if it exists. Returns True if removed."""
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def contains(self, item: Any) -> bool:
        """Check if item exists in the list."""
        return item in self._items

    def size(self) -> int:
        """Return the number of items in the list."""
        return len(self._items)

    def get_all(self) -> List[Any]:
        """Return a copy of all items."""
        return self._items.copy()


if __name__ == "__main__":
    try:
        manager = ListManager()
        manager.add_item("apple")
        manager.add_item("banana")
        print(f"Contains 'apple': {manager.contains('apple')}")
        print(f"Size: {manager.size()}")
        print(f"All items: {manager.get_all()}")
    except Exception as e:
        print(f"Error: {e}")