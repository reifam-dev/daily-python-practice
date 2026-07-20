# Day 66 - Clean contextlib examples
# New concepts: suppress, redirect_stdout, ExitStack, nullcontext
# PEP 8, docstrings, type hints, exceptions throughout

import contextlib
import io
import tempfile
from pathlib import Path


def demonstrate_suppress() -> None:
    """suppress() silently ignores specified exception types."""
    print("  Before suppress block")
    with contextlib.suppress(FileNotFoundError, PermissionError):
        open("definitely_does_not_exist_xyz.txt")
        print("  This line never runs")
    print("  After suppress block — no exception propagated\n")


def capture_output(func) -> str:
    """Capture stdout from a function using redirect_stdout."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func()
    return buffer.getvalue()


def demonstrate_exit_stack() -> None:
    """ExitStack allows dynamic stacking of context managers."""
    with tempfile.TemporaryDirectory() as tmp:
        filenames = [
            Path(tmp) / "report_a.txt",
            Path(tmp) / "report_b.txt",
            Path(tmp) / "report_c.txt",
        ]
        with contextlib.ExitStack() as stack:
            handles = [
                stack.enter_context(open(f, "w", encoding="utf-8"))
                for f in filenames
            ]
            for i, fh in enumerate(handles):
                fh.write(f"Content of report {i + 1}\n")

        print("  Files written and all handles closed cleanly:")
        for f in filenames:
            print(f"    {f.name}: {f.read_text(encoding='utf-8').strip()}")


def process_data(cm=None) -> str:
    """Use nullcontext as a no-op placeholder when no context manager needed."""
    context = cm if cm is not None else contextlib.nullcontext()
    with context:
        return "processed"


if __name__ == "__main__":
    print("=== contextlib.suppress ===\n")
    demonstrate_suppress()

    print("=== contextlib.redirect_stdout ===\n")
    def my_report():
        print("Line 1: Revenue up 12%")
        print("Line 2: Costs down 5%")
        print("Line 3: Net profit £2.4m")

    output = capture_output(my_report)
    print(f"  Captured {len(output.splitlines())} lines:")
    for line in output.splitlines():
        print(f"    {line}")

    print("\n=== contextlib.ExitStack ===\n")
    demonstrate_exit_stack()

    print("\n=== contextlib.nullcontext ===\n")
    result1 = process_data()
    result2 = process_data(contextlib.suppress(Exception))
    print(f"  Without cm : {result1}")
    print(f"  With cm    : {result2}")