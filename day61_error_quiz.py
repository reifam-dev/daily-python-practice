# Day 61 - Error Finding Quiz

from enum import Enum, auto

class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST  = auto()
    WEST  = auto()

class Colour(Enum):
    RED   = 1
    GREEN = 2
    BLUE  = 3

class Status(Enum):
    PENDING   = "pending"
    ACTIVE    = "active"
    CLOSED    = "closed"

# Bug 1 - accessing enum incorrectly
print(Direction.NORTH.value)   # correct
print(Direction.NORTH)         # correct
print(Direction["NORTH"])      # correct
print(Direction(1))            # correct
print(Direction.NORTH())       # Bug 1 - enums are not callable like this

# Bug 2 - comparison
d = Direction.NORTH
if d == "NORTH":               # Bug 2 - should compare to Direction.NORTH not string
    print("Heading north")

# Bug 3
for colour in Colour:
    print(colour.name, colour.value)

status = Status("active")      # correct - lookup by value
print(status.name)

# Bug 3 - cannot create duplicate values without alias decorator
class BadEnum(Enum):
    A = 1
    B = 1  # Bug 3 - B becomes alias for A silently, not a separate member
    C = 2

print(list(BadEnum))   # Only shows A and C, not B