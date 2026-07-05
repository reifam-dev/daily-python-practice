"""
Day 86 – Descriptor Protocol: __get__, __set__, __delete__, __set_name__.
Distinct from Day 38 (decorator syntax) and Day 49 (class-based decorators).
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

from typing import Any


class PositiveFloat:
    """Data descriptor that enforces positive numeric values."""

    def __set_name__(self, owner: type, name: str) -> None:
        """Store the attribute name when the descriptor is assigned to a class.

        Args:
            owner: The class that owns this descriptor.
            name:  The attribute name assigned to this descriptor.
        """
        self._name: str = name

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        """Return the stored value, or the descriptor itself if accessed on the class.

        Args:
            obj:     Instance the descriptor is accessed from, or None.
            objtype: Class of the instance.

        Returns:
            Stored float value or the descriptor object.
        """
        if obj is None:
            return self
        return obj.__dict__.get(self._name, 0.0)

    def __set__(self, obj: Any, value: float) -> None:
        """Validate and store a positive numeric value.

        Args:
            obj:   Instance to store the value on.
            value: Value to validate and store.

        Raises:
            TypeError:  If value is not numeric.
            ValueError: If value is negative.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name} must be numeric.")
        if value < 0:
            raise ValueError(f"{self._name} must be positive. Got {value}.")
        obj.__dict__[self._name] = value

    def __delete__(self, obj: Any) -> None:
        """Remove the stored value from the instance dictionary.

        Args:
            obj: Instance to remove the value from.
        """
        obj.__dict__.pop(self._name, None)


class ReadOnly:
    """Non-data descriptor that provides a read-only class-level constant."""

    def __init__(self, value: Any) -> None:
        """Initialise with the constant value to expose.

        Args:
            value: The read-only value.
        """
        self._value: Any = value

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        """Return the constant value regardless of access context.

        Args:
            obj:     Instance (ignored).
            objtype: Class (ignored).

        Returns:
            The stored constant value.
        """
        return self._value

    def __set__(self, obj: Any, value: Any) -> None:
        """Raise AttributeError — this attribute is read-only.

        Raises:
            AttributeError: Always.
        """
        raise AttributeError("Cannot set a read-only attribute.")

    def __delete__(self, obj: Any) -> None:
        """Raise AttributeError — this attribute cannot be deleted.

        Raises:
            AttributeError: Always.
        """
        raise AttributeError("Cannot delete a read-only attribute.")


class TypeEnforced:
    """Data descriptor that enforces a specific type on assignment."""

    def __init__(self, expected_type: type) -> None:
        """Initialise with the expected type.

        Args:
            expected_type: The type that values must be an instance of.
        """
        self._expected_type: type = expected_type
        self._name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Store the attribute name at class creation time.

        Args:
            owner: The class that owns this descriptor.
            name:  The attribute name assigned to this descriptor.
        """
        self._name = name

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        """Return the stored value or the descriptor itself.

        Args:
            obj:     Instance the descriptor is accessed from, or None.
            objtype: Class of the instance.

        Returns:
            Stored value or the descriptor object.
        """
        if obj is None:
            return self
        return obj.__dict__.get(self._name)

    def __set__(self, obj: Any, value: Any) -> None:
        """Validate type and store the value.

        Args:
            obj:   Instance to store the value on.
            value: Value to validate and store.

        Raises:
            TypeError: If value is not an instance of expected_type.
        """
        if not isinstance(value, self._expected_type):
            raise TypeError(
                f"{self._name} must be {self._expected_type.__name__}, "
                f"got {type(value).__name__}."
            )
        obj.__dict__[self._name] = value

    def __delete__(self, obj: Any) -> None:
        """Remove the stored value from the instance dictionary.

        Args:
            obj: Instance to remove the value from.
        """
        obj.__dict__.pop(self._name, None)


class PropertyDeal:
    """Real estate deal using descriptors for validated attributes."""

    value: float = PositiveFloat()
    yield_pct: float = PositiveFloat()
    sector: str = TypeEnforced(str)
    ASSET_CLASS = ReadOnly("Commercial Real Estate")

    def __init__(self, sector: str, value: float, yield_pct: float) -> None:
        """Initialise the deal with validated attributes.

        Args:
            sector:    Property sector string.
            value:     Deal value in £m (must be positive).
            yield_pct: Net initial yield as a percentage (must be positive).
        """
        self.sector = sector
        self.value = value
        self.yield_pct = yield_pct

    def capital_value(self) -> float:
        """Calculate capital value via direct capitalisation.

        Returns:
            Capital value in £m.
        """
        return self.value / (self.yield_pct / 100)

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this deal.
        """
        return (
            f"PropertyDeal(sector={self.sector!r}, "
            f"value={self.value}, yield_pct={self.yield_pct})"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation.

        Returns:
            User-facing string for this deal.
        """
        return (
            f"{self.sector} | £{self.value}m | "
            f"{self.yield_pct}% NIY | CV=£{self.capital_value():.1f}m"
        )


if __name__ == "__main__":
    deal = PropertyDeal("Office", 80.0, 4.5)
    print(deal)
    print(repr(deal))
    print(f"Asset class: {deal.ASSET_CLASS}")

    deal.value = 90.0
    print(f"\nUpdated: {deal}")

    print("\nTesting PositiveFloat validation:")
    try:
        deal.value = -10.0
    except ValueError as e:
        print(f"  Caught ValueError: {e}")

    try:
        deal.value = "eighty"
    except TypeError as e:
        print(f"  Caught TypeError: {e}")

    print("\nTesting TypeEnforced validation:")
    try:
        deal.sector = 123
    except TypeError as e:
        print(f"  Caught TypeError: {e}")

    print("\nTesting ReadOnly:")
    try:
        deal.ASSET_CLASS = "Residential"
    except AttributeError as e:
        print(f"  Caught AttributeError: {e}")

    print("\nTesting __delete__:")
    del deal.value
    print(f"  After del: value = {deal.value}")