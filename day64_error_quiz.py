# Day 64 - Error Finding Quiz

class SimpleCache:

    def __init__(self, max_size=5):
        self._store = {}
        self._max_size = max_size

    def __setitem__(self, key, value):
        if len(self._store) >= self._max_size:
            oldest = next(iter(self._store))
            del self._store[oldest]
        self._store[key] = value

    def __getitem__(self, key):
        if key not in self._store:
            raise KeyError(f"'{key}' not in cache.")
        return self._store[key]

    def __delitem__(self, key):
        del self._store[key]     # Bug 1 - no check if key exists

    def __len__(self):
        return len(self._store)

    def __contains__(self, key):
        return key in self._store


class Matrix:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self._data = [[0] * cols for _ in range(rows)]

    def __getitem__(self, index):
        row, col = index          # Bug 2 - no validation of index type or bounds
        return self._data[row][col]

    def __setitem__(self, index, value):
        row, col = index
        self._data[row][col] = value

    def __str__(self):
        return "\n".join(str(row) for row in self._data)


cache = SimpleCache(3)
cache["a"] = 1
cache["b"] = 2
cache["c"] = 3
cache["d"] = 4   # correct - evicts "a"
print("a" in cache)
print(len(cache))

del cache["z"]   # Bug 1 demonstrates here - KeyError

m = Matrix(3, 3)
m[0, 0] = 5
m[1, 1] = 10
print(m[0, 0])
print(m[5, 5])   # Bug 2 - IndexError, no bounds check