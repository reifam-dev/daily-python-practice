"""
Day 84 – python-dotenv and environment management: .env files, os.environ,
API key hygiene, validation, and .gitignore best practices.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
Requires: pip install python-dotenv

.env file example (never commit this to GitHub):
    ANTHROPIC_API_KEY=sk-ant-...
    DATABASE_URL=postgresql://user:pass@localhost:5432/property_db
    DEBUG=false
    LOG_LEVEL=INFO
    ENVIRONMENT=development

.gitignore must include:
    .env
    .env.*
    !.env.example
"""

import os
from dotenv import load_dotenv


class ApiConfig:
    """
    Manages application configuration loaded from a .env file.
    Provides validated, type-safe access to environment variables.
    Never logs or exposes raw API keys.
    """

    _REQUIRED_VARS: list[str] = ["ANTHROPIC_API_KEY", "DATABASE_URL"]

    def __init__(self, env_file: str = ".env") -> None:
        """Initialise configuration by loading the specified .env file.

        Args:
            env_file: Path to the .env file; defaults to '.env'.
        """
        load_dotenv(env_file, override=False)
        self._api_key: str | None = os.environ.get("ANTHROPIC_API_KEY")
        self._db_url: str | None = os.environ.get("DATABASE_URL")
        self._debug: str = os.environ.get("DEBUG", "false")
        self._log_level: str = os.environ.get("LOG_LEVEL", "INFO")
        self._environment: str = os.environ.get("ENVIRONMENT", "development")

    def get_api_key(self) -> str:
        """Return the Anthropic API key.

        Returns:
            API key string.

        Raises:
            ValueError: If ANTHROPIC_API_KEY is not set.
        """
        if not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment.")
        return self._api_key

    def get_db_url(self) -> str:
        """Return the database connection URL.

        Returns:
            Database URL string.

        Raises:
            ValueError: If DATABASE_URL is not set.
        """
        if not self._db_url:
            raise ValueError("DATABASE_URL not set in environment.")
        return self._db_url

    def is_debug(self) -> bool:
        """Return whether debug mode is enabled.

        Returns:
            True if DEBUG env var is set to 'true' (case-insensitive).
        """
        return self._debug.lower() == "true"

    def get_log_level(self) -> str:
        """Return the configured log level.

        Returns:
            Log level string (e.g. 'INFO', 'DEBUG').
        """
        return self._log_level.upper()

    def safe_get(self, key: str, default: str = "") -> str:
        """Safely retrieve any environment variable with a default.

        Args:
            key:     Environment variable name.
            default: Value to return if key is not set; defaults to ''.

        Returns:
            Environment variable value or default.
        """
        return os.environ.get(key, default)

    def mask_key(self, key: str) -> str:
        """Mask an API key for safe display in logs or repr.

        Args:
            key: Raw key string to mask.

        Returns:
            Masked string showing only the first 4 characters.
        """
        if len(key) < 8:
            return "***"
        return key[:4] + "*" * (len(key) - 4)

    def validate(self) -> bool:
        """Validate that all required environment variables are set.

        Returns:
            True if all required variables are present.

        Raises:
            EnvironmentError: If any required variables are missing.
        """
        missing = [k for k in self._REQUIRED_VARS if not os.environ.get(k)]
        if missing:
            raise EnvironmentError(f"Missing required env vars: {missing}")
        return True

    def as_dict(self) -> dict[str, str]:
        """Return a safe dictionary of configuration values (keys masked).

        Returns:
            Dictionary of config values with sensitive data masked.
        """
        return {
            "api_key": self.mask_key(self._api_key or ""),
            "db_url": self.mask_key(self._db_url or ""),
            "debug": str(self.is_debug()),
            "log_level": self.get_log_level(),
            "environment": self._environment,
        }

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string with masked sensitive values.
        """
        masked = self.mask_key(self._api_key or "")
        return (
            f"ApiConfig(api_key='{masked}', "
            f"environment='{self._environment}', "
            f"debug={self.is_debug()})"
        )


if __name__ == "__main__":
    config = ApiConfig()
    print(repr(config))
    print("\nConfig dict:")
    for key, value in config.as_dict().items():
        print(f"  {key}: {value}")
    print(f"\nDebug mode : {config.is_debug()}")
    print(f"Log level  : {config.get_log_level()}")
    print(f"DB URL     : {config.safe_get('DATABASE_URL', 'not configured')}")