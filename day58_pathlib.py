# Day 58 - Clean pathlib and file I/O examples
# New concepts: Path, read_text, write_text, glob, iterdir, exists
# PEP 8, docstrings, type hints, exceptions throughout

from pathlib import Path
from typing import List
import tempfile
import os


def demonstrate_path_operations() -> None:
    """Demonstrate Path construction and property access."""
    p = Path("data") / "reports" / "annual_report.txt"
    print(f"  Full path  : {p}")
    print(f"  Name       : {p.name}")
    print(f"  Stem       : {p.stem}")
    print(f"  Suffix     : {p.suffix}")
    print(f"  Parent     : {p.parent}")
    print(f"  Parts      : {p.parts}")


def write_and_read_file(path: Path, content: str) -> str:
    """Write content to a file and read it back."""
    path.write_text(content, encoding="utf-8")
    return path.read_text(encoding="utf-8")


def read_lines(path: Path) -> List[str]:
    """Read a file and return its lines as a list."""
    return path.read_text(encoding="utf-8").splitlines()


def count_files_by_extension(directory: Path, extension: str) -> int:
    """Count files with a given extension in a directory tree."""
    return len(list(directory.glob(f"**/*{extension}")))


if __name__ == "__main__":
    print("=== Path operations ===\n")
    demonstrate_path_operations()

    print("\n=== Write and read file ===\n")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        report = tmp_path / "report.txt"
        content = "Line 1: Revenue\nLine 2: Costs\nLine 3: Profit"
        result = write_and_read_file(report, content)
        print(f"  Written and read back:\n  {result}\n")

        lines = read_lines(report)
        print(f"  Lines ({len(lines)}):")
        for line in lines:
            print(f"    {line}")

        print(f"\n  report.exists()  : {report.exists()}")
        print(f"  report.is_file() : {report.is_file()}")
        print(f"  report.is_dir()  : {report.is_dir()}")
        print(f"  report.stat().st_size : {report.stat().st_size} bytes")

        print("\n=== iterdir — list directory contents ===\n")
        (tmp_path / "notes.txt").write_text("notes")
        (tmp_path / "data.csv").write_text("a,b,c")
        for item in sorted(tmp_path.iterdir()):
            print(f"  {'DIR' if item.is_dir() else 'FILE'}: {item.name}")

        print("\n=== glob — find files by pattern ===\n")
        txt_count = count_files_by_extension(tmp_path, ".txt")
        print(f"  .txt files found : {txt_count}")