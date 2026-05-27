# Day 46 - Clean Singleton pattern
# New concepts: __new__, Singleton pattern, single instance control
# PEP 8, docstrings, type hints, exceptions throughout

from typing import Optional, Any


class DatabaseSingleton:
    """Singleton database connection manager.

    Uses __new__ to ensure only one instance is ever created.
    __init__ guard prevents re-initialisation on subsequent calls.
    """

    _instance: Optional["DatabaseSingleton"] = None
    _initialised: bool = False

    def __new__(cls) -> "DatabaseSingleton":
        """Create instance only if one does not already exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str = "localhost", port: int = 5432) -> None:
        """Initialise only on first creation — guard prevents re-init."""
        if self._initialised:
            return
        self._host = host
        self._port = port
        self._connected = False
        DatabaseSingleton._initialised = True

    def connect(self) -> str:
        """Simulate connecting to the database."""
        self._connected = True
        return f"Connected to {self._host}:{self._port}"

    def disconnect(self) -> str:
        """Simulate disconnecting from the database."""
        self._connected = False
        return f"Disconnected from {self._host}:{self._port}"

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def connected(self) -> bool:
        return self._connected

    def __str__(self) -> str:
        return (f"DatabaseSingleton("
                f"host='{self._host}', "
                f"port={self._port}, "
                f"connected={self._connected})")


class ConfigSingleton:
    """Singleton configuration manager.

    Stores application settings as key-value pairs.
    Only one instance exists throughout the programme lifetime.
    """

    _instance: Optional["ConfigSingleton"] = None
    _initialised: bool = False

    def __new__(cls) -> "ConfigSingleton":
        """Create instance only if one does not already exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialise only on first creation."""
        if self._initialised:
            return
        self._settings: dict = {}
        ConfigSingleton._initialised = True

    def set(self, key: str, value: Any) -> None:
        """Store a setting."""
        self._settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a setting, returning default if not found."""
        return self._settings.get(key, default)

    def get_all(self) -> dict:
        """Return a copy of all settings."""
        return self._settings.copy()

    def __str__(self) -> str:
        return f"ConfigSingleton(settings={self._settings})"


if __name__ == "__main__":
    print("=== DatabaseSingleton ===\n")
    db1 = DatabaseSingleton("localhost", 5432)
    db2 = DatabaseSingleton("remotehost", 9999)

    print(f"db1 is db2       : {db1 is db2}")
    print(f"db1 host         : {db1.host}")
    print(f"db2 host         : {db2.host}")
    print(f"{db1.connect()}")
    print(f"db1              : {db1}\n")

    print("=== ConfigSingleton ===\n")
    config1 = ConfigSingleton()
    config1.set("theme", "dark")
    config1.set("language", "en-GB")

    config2 = ConfigSingleton()
    print(f"config1 is config2  : {config1 is config2}")
    print(f"config2 theme       : {config2.get('theme')}")
    print(f"All settings        : {config2.get_all()}")