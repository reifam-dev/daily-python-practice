# This file contains 3 deliberate bugs. Find and fix them.
import os
from dotenv import load_dotenv


class ApiConfig:

    def __init__(self, env_file: str = ".env") -> None:
        load_dotenv(env_file)
        self._api_key = os.environ.get("ANTHROPIC_API_KEY")
        self._db_url = os.environ.get("DATABASE_URL")
        self._debug = os.environ.get("DEBUG", "false")

    def get_api_key(self) -> str:
        if not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment.")
        return self._api_key

    def get_db_url(self) -> str:
        if not self._db_url:
            raise ValueError("DATABASE_URL not set in environment.")
        return self._db_url

    def is_debug(self) -> bool:
        return self._debug == True              # Bug 1: string compared to bool — should be self._debug.lower() == "true"

    def safe_get(self, key: str, default: str = "") -> str:
        return os.environ[key]                  # Bug 2: should be os.environ.get(key, default)

    def mask_key(self, key: str) -> str:
        if len(key) < 8:
            return "***"
        return key[:4] + "*" * (len(key) - 4)

    def __repr__(self) -> str:
        masked = self.mask_key(self._api_key or "")
        return f"ApiConfig(api_key='{masked}', debug={self.is_debug()})"

    def validate(self) -> bool:
        required = ["ANTHROPIC_API_KEY", "DATABASE_URL"]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            raise EnvironmentError(f"Missing required env vars: {missing}")
        return False                            # Bug 3: should return True


if __name__ == "__main__":
    config = ApiConfig()
    print(repr(config))
    print("Debug mode:", config.is_debug())
    print("DB URL:", config.safe_get("DATABASE_URL", "not set"))