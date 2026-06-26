"""
Day 76 – Docker Basics: Dockerfile generation, CLI commands, docker-compose snippet.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

from dataclasses import dataclass, field


@dataclass
class DockerConfig:
    """Configuration for a Docker image build."""

    image_name: str
    python_version: str = "3.12"
    port: int = 8000
    workdir: str = "/app"
    entrypoint: str = "main.py"
    env_vars: dict[str, str] = field(default_factory=dict)


class DockerManager:
    """Generates Dockerfile content and Docker CLI commands for a Python service."""

    def __init__(self, config: DockerConfig) -> None:
        """Initialise with a DockerConfig instance.

        Args:
            config: Configuration dataclass for the Docker image.
        """
        self._config: DockerConfig = config

    def generate_dockerfile(self) -> str:
        """Generate a production-ready Dockerfile as a string.

        Returns:
            Multi-line Dockerfile content.
        """
        lines: list[str] = [
            f"FROM python:{self._config.python_version}-slim",
            f"WORKDIR {self._config.workdir}",
            "COPY requirements.txt .",
            "RUN pip install --no-cache-dir -r requirements.txt",
            "COPY . .",
            f"EXPOSE {self._config.port}",
        ]
        for key, value in self._config.env_vars.items():
            lines.append(f"ENV {key}={value}")
        lines.append(f'CMD ["python", "{self._config.entrypoint}"]')
        return "\n".join(lines)

    def build_command(self, tag: str = "latest") -> str:
        """Produce the docker build CLI command.

        Args:
            tag: Image tag; defaults to 'latest'.

        Returns:
            Docker build command string.
        """
        return f"docker build -t {self._config.image_name}:{tag} ."

    def run_command(self, detached: bool = True) -> str:
        """Produce the docker run CLI command.

        Args:
            detached: If True, add -d flag for detached mode.

        Returns:
            Docker run command string.
        """
        flag = "-d " if detached else ""
        port = self._config.port
        return f"docker run {flag}-p {port}:{port} {self._config.image_name}"

    def compose_snippet(self) -> str:
        """Generate a minimal docker-compose.yml snippet for this service.

        Returns:
            docker-compose YAML content as a string.
        """
        port = self._config.port
        return (
            "services:\n"
            f"  {self._config.image_name}:\n"
            f"    build: .\n"
            f"    ports:\n"
            f"      - '{port}:{port}'\n"
        )

    def __len__(self) -> int:
        """Return the length of the image name.

        Returns:
            Integer length of the image name string.
        """
        return len(self._config.image_name)

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this DockerManager.
        """
        return (
            f"DockerManager(image='{self._config.image_name}', "
            f"port={self._config.port})"
        )


if __name__ == "__main__":
    config = DockerConfig(
        image_name="realestate-api",
        python_version="3.12",
        port=8000,
        entrypoint="main.py",
        env_vars={"ENV": "production", "LOG_LEVEL": "INFO"},
    )
    dm = DockerManager(config)

    print("=== Dockerfile ===")
    print(dm.generate_dockerfile())
    print("\n=== Build Command ===")
    print(dm.build_command("v1.0"))
    print("\n=== Run Command ===")
    print(dm.run_command())
    print("\n=== Compose Snippet ===")
    print(dm.compose_snippet())
    print(repr(dm))