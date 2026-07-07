"""
Day 88 – Metaclasses and class internals: SingletonMeta, RegistryMeta, ValidatedMeta.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

from typing import Any


class SingletonMeta(type):
    """Metaclass that enforces the Singleton pattern for any class using it."""

    _instances: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Return the existing instance or create one if none exists.

        Returns:
            The single instance of the class.
        """
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMeta._instances[cls]


class RegistryMeta(type):
    """Metaclass that automatically registers all subclasses in a class registry."""

    _registry: dict[str, type] = {}

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        """Create the class and register it if it is not the base class.

        Args:
            name:      Class name.
            bases:     Tuple of base classes.
            namespace: Class namespace dictionary.

        Returns:
            Newly created class.
        """
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "BaseAsset":
            RegistryMeta._registry[name] = cls
        return cls

    @classmethod
    def get_registry(mcs) -> dict[str, type]:
        """Return a copy of the class registry.

        Returns:
            Dictionary mapping class names to class objects.
        """
        return dict(mcs._registry)


class ValidatedMeta(type):
    """Metaclass that validates class attributes at class creation time."""

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        """Raise ValueError if any non-dunder numeric attribute is negative.

        Args:
            name:      Class name.
            bases:     Tuple of base classes.
            namespace: Class namespace dictionary.

        Returns:
            Newly created class.

        Raises:
            ValueError: If any numeric non-dunder attribute is negative.
        """
        for attr, value in namespace.items():
            if attr.startswith("__"):
                continue
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(
                    f"Negative class attribute not permitted: {attr}={value}"
                )
        return super().__new__(mcs, name, bases, namespace)


# ── Classes using metaclasses ─────────────────────────────────────────────────

class BaseAsset(metaclass=RegistryMeta):
    """Base class for all registered asset types."""
    pass


class OfficeAsset(BaseAsset):
    """Registered office asset type."""
    sector: str = "Office"
    typical_yield: float = 0.045


class RetailAsset(BaseAsset):
    """Registered retail asset type."""
    sector: str = "Retail"
    typical_yield: float = 0.055


class IndustrialAsset(BaseAsset):
    """Registered industrial asset type."""
    sector: str = "Industrial"
    typical_yield: float = 0.050


class PropertyFund(metaclass=ValidatedMeta):
    """Fund configuration validated at class creation time."""
    target_return: float = 0.08
    max_ltv: float = 0.65
    min_yield: float = 0.045


class DatabaseConfig(metaclass=SingletonMeta):
    """Singleton database configuration object."""

    def __init__(self, host: str, port: int) -> None:
        """Initialise with host and port (only runs once due to Singleton).

        Args:
            host: Database host string.
            port: Database port number.
        """
        self.host: str = host
        self.port: int = port

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this config.
        """
        return f"DatabaseConfig(host={self.host!r}, port={self.port})"


if __name__ == "__main__":
    print("=== Registry ===")
    print(RegistryMeta.get_registry())

    print("\n=== Singleton ===")
    db1 = DatabaseConfig("localhost", 5432)
    db2 = DatabaseConfig("remotehost", 5433)
    print(f"db1: {db1}")
    print(f"db2: {db2}")
    print(f"Same instance: {db1 is db2}")

    print("\n=== Validated class attributes ===")
    print(f"PropertyFund.target_return = {PropertyFund.target_return}")

    try:
        class BadFund(metaclass=ValidatedMeta):
            target_return = -0.05
    except ValueError as e:
        print(f"Caught: {e}")

    print("\n=== Asset types ===")
    for name, cls in RegistryMeta.get_registry().items():
        print(f"  {name}: sector={getattr(cls, 'sector', 'N/A')}")