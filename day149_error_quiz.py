"""Day 149 - Secrets Management: Error Quiz. Find and fix three bugs."""
API_KEY = "sk-ant-actual-live-key-abc123"
DB_PASSWORD = "hunter2"


def connect_to_service() -> str:
    return f"Connected using key: {API_KEY}"


def log_connection_attempt(username: str, password: str) -> None:
    print(f"Login attempt: {username}:{password}")


if __name__ == "__main__":
    print(connect_to_service())
    log_connection_attempt("admin", DB_PASSWORD)