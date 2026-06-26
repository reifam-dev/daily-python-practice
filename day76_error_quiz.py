# This file contains 3 deliberate bugs. Find and fix them.
import shlex


class DockerManager:

    def __init__(self, image_name: str) -> None:
        self._image_name = image_name

    def build_image(self, tag: str = "latest") -> str:
        cmd = f"docker build -t {self._image_name}:{tag}"  # Bug 1: missing trailing .
        return cmd

    def run_container(self, port: int = 8000) -> str:
        cmd = f"docker run -p {port}:{port} {self._image_name}"
        return cmd

    def stop_container(self, container_id: str) -> str:
        parts = shlex.split(f"docker stop {container_id}")
        return " ".join(parts)

    def generate_dockerfile(self, python_version: str = "3.12") -> str:
        lines = [
            f"FROM python:{python_version}-slim",
            "WORKDIR /app",
            "COPY requirements.txt .",
            "RUN pip install -r requirements.txt",
            "COPY . .",
            "EXPOSE 8000",
            'CMD ["python", "main.py"]',
        ]
        return "/n".join(lines)                # Bug 2: "/n" should be "\n"

    def compose_snippet(self, port: int = 8000) -> str:
        return (
            "services:\n"
            f"  {self._image_name}:\n"
            f"    build: .\n"
            f"    ports:\n"
            f"      - '{port}:{port}'\n"
        )

    def __repr__(self) -> str:
        return f"DockerManager(image_name={self._image_name!r})"

    def __len__(self) -> int:
        return len(self._image_name) + 100     # Bug 3: should just be len(self._image_name)


if __name__ == "__main__":
    dm = DockerManager("realestate-api")
    print(dm.build_image())
    print(dm.generate_dockerfile())
    print(dm.compose_snippet())
    print(len(dm))