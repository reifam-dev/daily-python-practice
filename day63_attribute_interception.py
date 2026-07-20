# Day 63 - Clean __getattr__ and __setattr__ examples
# New concepts: __getattr__, __setattr__, __delattr__, attribute interception
# PEP 8, docstrings, type hints, exceptions throughout

from typing import Any, List, Set


class ValidatedRecord:
    """A record that only allows a fixed set of field names.

    __setattr__ intercepts all attribute assignments.
    __getattr__ is only called when normal attribute lookup fails.

    Key rule: use object.__setattr__ to avoid infinite recursion
    when setting attributes inside __setattr__ itself.
    """

    _ALLOWED_FIELDS: Set[str] = {"name", "age", "salary"}

    def __init__(self) -> None:
        # Use object.__setattr__ to bypass our own __setattr__
        object.__setattr__(self, "_data", {})

    def __setattr__(self, name: str, value: Any) -> None:
        """Only allow setting fields in _ALLOWED_FIELDS."""
        if name not in self._ALLOWED_FIELDS:
            raise AttributeError(
                f"'{name}' is not an allowed field. "
                f"Allowed: {sorted(self._ALLOWED_FIELDS)}"
            )
        self._data[name] = value

    def __getattr__(self, name: str) -> Any:
        """Called only when normal lookup fails — field not yet set."""
        if name in self._ALLOWED_FIELDS:
            return f"'{name}' has not been set."
        raise AttributeError(f"'{name}' is not a recognised field.")

    def __repr__(self) -> str:
        return f"ValidatedRecord({self._data})"


class LoggedObject:
    """An object that logs every attribute set operation.

    Demonstrates using self.__dict__ directly inside __setattr__
    to avoid infinite recursion.
    """

    def __init__(self) -> None:
        self.__dict__["_log"]: List[str] = []

    def __setattr__(self, name: str, value: Any) -> None:
        """Log the assignment then store it."""
        self.__dict__["_log"].append(f"SET {name} = {value!r}")
        self.__dict__[name] = value

    def __getattr__(self, name: str) -> Any:
        """Called when attribute not found — raise descriptive error."""
        raise AttributeError(f"'{name}' has not been set on this object.")

    def get_log(self) -> List[str]:
        """Return a copy of the attribute change log."""
        return self._log.copy()

    def __repr__(self) -> str:
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return f"LoggedObject({data})"


class FrozenObject:
    """An immutable object — all fields set at creation, none changeable after.

    Uses object.__setattr__ in __init__ to bypass the frozen check.
    """

    def __init__(self, **kwargs: Any) -> None:
        for key, val in kwargs.items():
            object.__setattr__(self, key, val)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(
            f"Cannot set '{name}' — this object is frozen."
        )

    def __delattr__(self, name: str) -> None:
        raise AttributeError(
            f"Cannot delete '{name}' — this object is frozen."
        )

    def __repr__(self) -> str:
        return f"FrozenObject({self.__dict__})"


if __name__ == "__main__":
    print("=== ValidatedRecord ===\n")
    rec = ValidatedRecord()
    rec.name = "Alice"
    rec.age = 30
    rec.salary = 75000.0
    print(f"  Record  : {rec}")
    print(f"  name    : {rec.name}")
    print(f"  missing : {rec.missing_field}")

    try:
        rec.email = "alice@example.com"
    except AttributeError as e:
        print(f"  Error   : {e}\n")

    print("=== LoggedObject ===\n")
    obj = LoggedObject()
    obj.name = "Bob"
    obj.age = 25
    obj.name = "Robert"
    print(f"  Object  : {obj}")
    print("  Log     :")
    for entry in obj.get_log():
        print(f"    {entry}")

    print("\n=== FrozenObject ===\n")
    point = FrozenObject(x=3, y=4)
    print(f"  Point   : {point}")
    print(f"  x       : {point.x}")

    try:
        point.x = 10
    except AttributeError as e:
        print(f"  Error   : {e}")

    try:
        del point.x
    except AttributeError as e:
        print(f"  Error   : {e}")