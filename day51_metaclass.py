# Day 51 - Clean metaclass examples
# New concepts: type, metaclass, __new__ in metaclass, dynamic class creation
# PEP 8, docstrings, type hints, exceptions throughout

from __future__ import annotations
from typing import Any, Dict, Tuple


class SingletonMeta(type):
    """Metaclass that implements the Singleton pattern.

    Any class using metaclass=SingletonMeta will only
    ever have one instance created.
    """

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Create instance only if one does not already exist."""
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMeta._instances[cls]


class ValidatedMeta(type):
    """Metaclass that enforces docstrings on all public methods.

    Raises TypeError at class creation time if any public
    method is missing a docstring.
    """

    def __new__(
        mcs,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any]
    ) -> "ValidatedMeta":
        """Validate all public methods have docstrings before creating class."""
        for key, value in namespace.items():
            if callable(value) and not key.startswith('_'):
                if not value.__doc__:
                    raise TypeError(
                        f"Method '{key}' in class '{name}' "
                        f"must have a docstring."
                    )
        return super().__new__(mcs, name, bases, namespace)


class Database(metaclass=SingletonMeta):
    """A singleton database connection.

    Only one instance is ever created regardless of how many
    times the class is instantiated.
    """

    _initialised: bool = False

    def __init__(self, host: str = "localhost", port: int = 5432) -> None:
        """Initialise only on first creation."""
        if self._initialised:
            return
        self._host = host
        self._port = port
        Database._initialised = True

    @property
    def host(self) -> str:
        """Return the database host."""
        return self._host

    @property
    def port(self) -> int:
        """Return the database port."""
        return self._port

    def connect(self) -> str:
        """Return a connection string."""
        return f"Connected to {self._host}:{self._port}"

    def __str__(self) -> str:
        """Return a string representation."""
        return f"Database('{self._host}', {self._port})"


class Config(metaclass=ValidatedMeta):
    """A validated configuration class.

    All public methods must have docstrings — enforced by ValidatedMeta.
    """

    def __init__(self) -> None:
        """Initialise with an empty settings dictionary."""
        self._settings: Dict[str, Any] = {}

    def get_setting(self, key: str) -> Any:
        """Return the value for the given key, or None if not found."""
        return self._settings.get(key)

    def set_setting(self, key: str, value: Any) -> None:
        """Store a key-value setting."""
        self._settings[key] = value

    def get_all(self) -> Dict[str, Any]:
        """Return a copy of all settings."""
        return self._settings.copy()


if __name__ == "__main__":
    print("=== SingletonMeta ===\n")
    db1 = Database("localhost", 5432)
    db2 = Database("remotehost", 9999)

    print(f"  db1 is db2   : {db1 is db2}")
    print(f"  db1 host     : {db1.host}")
    print(f"  db2 host     : {db2.host}")
    print(f"  {db1.connect()}\n")

    print("=== ValidatedMeta ===\n")
    config = Config()
    config.set_setting("theme", "dark")
    config.set_setting("language", "en-GB")
    print(f"  theme    : {config.get_setting('theme')}")
    print(f"  all      : {config.get_all()}\n")

    print("=== Dynamic class creation with type() ===\n")
    DynamicPoint = type("DynamicPoint", (object,), {
        "__init__": lambda self, x, y: setattr(self, 'x', x) or setattr(self, 'y', y),
        "__str__": lambda self: f"DynamicPoint({self.x}, {self.y})",
        "distance": lambda self: (self.x ** 2 + self.y ** 2) ** 0.5
    })

    p = DynamicPoint(3, 4)
    print(f"  {p}")
    print(f"  Distance : {p.distance():.2f}")
    print(f"  Type     : {type(p)}")
    print(f"  MRO      : {[c.__name__ for c in type(p).__mro__]}")

    print("\n=== ValidatedMeta enforcement ===\n")
    try:
        class BadClass(metaclass=ValidatedMeta):
            def missing_docstring(self):
                pass
    except TypeError as e:
        print(f"  TypeError: {e}")