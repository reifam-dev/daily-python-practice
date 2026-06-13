# Day 64 - Clean __getitem__, __setitem__, __delitem__ container protocol
# New concepts: container protocol, custom indexing, matrix access
# PEP 8, docstrings, type hints, exceptions throughout

from typing import Any, Tuple


class SimpleCache:
    """An LRU-style cache with a maximum size.

    Implements the container protocol — supports obj[key],
    obj[key] = value, del obj[key], len(obj) and key in obj.
    When full, the oldest item is evicted on insertion.
    """

    def __init__(self, max_size: int = 5) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive.")
        self._store: dict = {}
        self._max_size = max_size

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set a key. Evicts oldest if at capacity."""
        if key in self._store:
            del self._store[key]
        elif len(self._store) >= self._max_size:
            oldest = next(iter(self._store))
            del self._store[oldest]
        self._store[key] = value

    def __getitem__(self, key: Any) -> Any:
        """Get a value by key. Raises KeyError if not found."""
        if key not in self._store:
            raise KeyError(f"'{key}' not in cache.")
        return self._store[key]

    def __delitem__(self, key: Any) -> None:
        """Delete a key. Raises KeyError if not found."""
        if key not in self._store:
            raise KeyError(f"'{key}' not in cache.")
        del self._store[key]

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return len(self._store)

    def __contains__(self, key: Any) -> bool:
        """Enable the 'in' operator."""
        return key in self._store

    def __repr__(self) -> str:
        return f"SimpleCache({self._store}, max={self._max_size})"


class Matrix:
    """A 2D matrix supporting row/column indexing via tuples.

    Usage:
        m = Matrix(3, 3)
        m[0, 0] = 5       # __setitem__ with tuple key
        val = m[0, 0]     # __getitem__ with tuple key
    """

    def __init__(self, rows: int, cols: int) -> None:
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and cols must be positive.")
        self._rows = rows
        self._cols = cols
        self._data = [[0] * cols for _ in range(rows)]

    def _validate(self, index: Tuple[int, int]) -> Tuple[int, int]:
        """Validate and return (row, col). Raises IndexError if out of bounds."""
        if not isinstance(index, tuple) or len(index) != 2:
            raise TypeError("Index must be a (row, col) tuple.")
        row, col = index
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(
                f"Index ({row}, {col}) out of bounds for "
                f"{self._rows}x{self._cols} matrix."
            )
        return row, col

    def __getitem__(self, index: Tuple[int, int]) -> int:
        """Get value at (row, col)."""
        row, col = self._validate(index)
        return self._data[row][col]

    def __setitem__(self, index: Tuple[int, int], value: int) -> None:
        """Set value at (row, col)."""
        row, col = self._validate(index)
        self._data[row][col] = value

    def __str__(self) -> str:
        return "\n".join("  " + str(row) for row in self._data)

    def __repr__(self) -> str:
        return f"Matrix({self._rows}x{self._cols})"


if __name__ == "__main__":
    print("=== SimpleCache ===\n")
    cache = SimpleCache(3)
    cache["a"] = 1
    cache["b"] = 2
    cache["c"] = 3
    print(f"  Cache     : {cache}")
    print(f"  'a' in cache: {'a' in cache}")
    print(f"  Length    : {len(cache)}")

    cache["d"] = 4
    print(f"  After adding 'd' (evicts 'a'): {cache}")
    print(f"  'a' in cache: {'a' in cache}")

    try:
        print(cache["z"])
    except KeyError as e:
        print(f"  KeyError  : {e}")

    try:
        del cache["z"]
    except KeyError as e:
        print(f"  Delete KeyError: {e}\n")

    print("=== Matrix ===\n")
    m = Matrix(3, 3)
    m[0, 0] = 5
    m[1, 1] = 10
    m[2, 2] = 15
    print(f"  Matrix:\n{m}")
    print(f"\n  m[1,1]    : {m[1, 1]}")

    try:
        print(m[5, 5])
    except IndexError as e:
        print(f"  IndexError: {e}")