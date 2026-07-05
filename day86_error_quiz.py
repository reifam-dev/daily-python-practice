# This file contains 3 deliberate bugs. Find and fix them.
from typing import Any


class PositiveFloat:

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: Any, objtype: Any = None) -> float:
        if obj is None:
            return self                         # Bug 1: should return self (correct) — actual bug: missing return type Any
        return obj.__dict__.get(self._name, 0.0)

    def __set__(self, obj: Any, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name} must be numeric.")
        if value < 0:
            raise ValueError(f"{self._name} must be positive.")
        obj.__dict__[self._name] == value       # Bug 2: == should be =


class ReadOnly:

    def __init__(self, value: Any) -> None:
        self._value = value

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        return self._value

    def __set__(self, obj: Any, value: Any) -> None:
        raise AttributeError(f"Cannot set read-only attribute.")

    def __delete__(self, obj: Any) -> None:
        raise AttributeError(f"Cannot delete read-only attribute.")


class TypeEnforced:

    def __init__(self, expected_type: type) -> None:
        self._expected_type = expected_type

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        if obj is None:
            return self
        return obj.__dict__.get(self._name)

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, self._expected_type):
            raise TypeError(
                f"{self._name} must be {self._expected_type.__name__}, "
                f"got {type(value).__name__}."
            )
        obj.__dict__[self._name] = value


class PropertyDeal:

    value = PositiveFloat()
    yield_pct = PositiveFloat()
    sector = TypeEnforced(str)
    ASSET_CLASS = ReadOnly("Commercial Real Estate")

    def __init__(self, sector: str, value: float, yield_pct: float) -> None:
        self.sector = sector
        self.value = value
        self.yield_pct = yield_pct

    def capital_value(self) -> float:
        return self.value / (self.yield_pct / 100)

    def __repr__(self) -> str:
        return f"PropertyDeal(sector={self.sector!r}, value={self.value}, yield_pct={self.yield_pct})"

    def __str__(self) -> str:
        return f"{self.sector} | £{self.value}m | {self.yield_pct}% NIY | CV=£{self.capital_value():.1f}m"


if __name__ == "__main__":
    deal = PropertyDeal("Office", 80.0, 4.5)
    print(deal)
    print(repr(deal))
    print(deal.ASSET_CLASS)
    try:
        deal.value = -10.0
    except ValueError as e:
        print(f"Caught: {e}")
    try:
        deal.ASSET_CLASS = "Residential"       # Bug 3: should raise AttributeError — works; actual Bug 3: __delete__ not tested — real Bug 3 is ReadOnly.__set__ missing self._name reference
    except AttributeError as e:
        print(f"Caught: {e}")