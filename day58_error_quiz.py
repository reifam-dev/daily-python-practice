# Day 58 - Error Finding Quiz

from pathlib import Path

# Path creation
p = Path("data") / "files" / "report.txt"
print(p)
print(p.name)
print(p.stem)
print(p.suffix)
print(p.parent)

# Writing a file
output = Path("output.txt")
output.write_text("Hello, World!")

# Reading a file
content = output.read_text
print(content)                          # Bug 1 - missing ()

# Path checks
print(output.exists())
print(output.is_file())
print(output.is_dir())

# Reading lines
lines_path = Path("output.txt")
lines_path.write_text("line1\nline2\nline3")
lines = lines_path.read_text.splitlines()  # Bug 2 - missing ()

# Using open()
with open(output, "r") as f:
    data = f.read()

# glob
fake_dir = Path(".")
py_files = list(fake_dir.glob("**/*.py"))
print(len(py_files))

# Bug 3 - iterating Path incorrectly
for item in Path:                       # Bug 3 - should be Path(".") or a Path instance
    print(item)