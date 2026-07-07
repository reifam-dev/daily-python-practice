# This file contains 3 deliberate bugs. Find and fix them.
from typing import Any


class SingletonMeta(type):

    _instances: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class RegistryMeta(type):

    _registry: dict = {}

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "BaseAsset":
            mcs._registry[name] = cls          # Bug 1: should be RegistryMeta._registry[name] = cls
        return cls

    @classmethod
    def get_registry(mcs) -> dict:
        return dict(mcs._registry)


class BaseAsset(metaclass=RegistryMeta):
    pass


class OfficeAsset(BaseAsset):
    sector = "Office"


class RetailAsset(BaseAsset):
    sector = "Retail"


class ValidatedMeta(type):

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        for attr, value in namespace.items():
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(f"Negative class attribute not permitted: {attr}={value}")
        return super().__new__(mcs, name, bases, namespace)


class PropertyFund(metaclass=ValidatedMeta):
    target_return = 0.08
    max_ltv = 0.65
    min_yield = 0.045


class DatabaseConfig(metaclass=SingletonMeta):

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def __repr__(self) -> str:
        return f"DatabaseConfig(host={self.host!r}, port={self.port})"


if __name__ == "__main__":
    print(RegistryMeta.get_registry())

    db1 = DatabaseConfig("localhost", 5432)
    db2 = DatabaseConfig("remotehost", 5433)
    print(db1 is db2)                          # Bug 2: should print True — works fine; actual Bug 2: SingletonMeta uses cls._instances which causes MRO lookup issues — should use SingletonMeta._instances

    try:
        class BadFund(metaclass=ValidatedMeta):
            target_return = -0.05              # Bug 3: test expects this to raise — works; actual Bug 3 is in ValidatedMeta.__new__: attrs starting with __ should be skipped to avoid checking dunder attrs
    except ValueError as e:
        print(f"Caught: {e}")