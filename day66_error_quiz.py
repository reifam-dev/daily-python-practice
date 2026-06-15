# Day 66 - Error Finding Quiz

import contextlib
import io

# suppress — silently ignores specified exceptions
with contextlib.suppress(FileNotFoundError):
    open("nonexistent.txt")   # correct - exception suppressed

# redirect_stdout
f = io.StringIO()
with contextlib.redirect_stdout(f):
    print("captured output")

output = f.getvalue
print(output)               # Bug 1 - missing ()

# ExitStack - dynamic context manager stacking
files = []
with contextlib.ExitStack() as stack:
    for name in ["a.txt", "b.txt"]:
        f = stack.enter_context(open(name, "w"))
        files.append(f)
        f.write(f"content of {name}")
    # Bug 2 - files may not exist, should use tempfile

# nullcontext
def process(cm=None):
    with cm or contextlib.nullcontext():  # Bug 3 - nullcontext needs ()
        print("processing")

process()