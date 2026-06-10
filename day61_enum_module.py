# Day 61 - Clean enum module examples
# New concepts: Enum, auto(), value access, iteration, aliases, Flag
# PEP 8, docstrings, type hints, exceptions throughout

from enum import Enum, auto, Flag, unique
from typing import List


@unique
class Direction(Enum):
    """Cardinal directions. @unique prevents accidental value duplicates."""
    NORTH = auto()
    SOUTH = auto()
    EAST  = auto()
    WEST  = auto()

    def opposite(self) -> "Direction":
        """Return the opposite direction."""
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST:  Direction.WEST,
            Direction.WEST:  Direction.EAST,
        }
        return opposites[self]

    def __str__(self) -> str:
        return self.name.capitalize()


class Status(Enum):
    """Transaction status with string values."""
    PENDING  = "pending"
    ACTIVE   = "active"
    CLOSED   = "closed"
    REJECTED = "rejected"

    @classmethod
    def from_string(cls, value: str) -> "Status":
        """Create Status from a string value. Raises ValueError if not found."""
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(
                f"'{value}' is not a valid Status. "
                f"Valid values: {[s.value for s in cls]}"
            )

    def is_terminal(self) -> bool:
        """Return True if this is a final state."""
        return self in (Status.CLOSED, Status.REJECTED)


class Permission(Flag):
    """File permissions using Flag — supports bitwise combination."""
    READ    = auto()
    WRITE   = auto()
    EXECUTE = auto()
    NONE    = 0


if __name__ == "__main__":
    print("=== Direction Enum ===\n")
    d = Direction.NORTH
    print(f"  Value       : {d.value}")
    print(f"  Name        : {d.name}")
    print(f"  str         : {d}")
    print(f"  Opposite    : {d.opposite()}")
    print(f"  Is Enum     : {isinstance(d, Direction)}")
    print(f"  By name     : {Direction['EAST']}")
    print(f"  By value    : {Direction(2)}")

    print(f"\n  All directions:")
    for direction in Direction:
        print(f"    {direction.name} = {direction.value}")

    print("\n=== Status Enum ===\n")
    s = Status.from_string("active")
    print(f"  Status      : {s}")
    print(f"  Terminal    : {s.is_terminal()}")
    print(f"  Closed terminal: {Status.CLOSED.is_terminal()}")

    print("\n=== Enum comparison ===\n")
    print(f"  NORTH == NORTH : {Direction.NORTH == Direction.NORTH}")
    print(f"  NORTH is NORTH : {Direction.NORTH is Direction.NORTH}")
    print(f"  NORTH == 'NORTH': {Direction.NORTH == 'NORTH'}")

    print("\n=== Permission Flag (bitwise) ===\n")
    user_perms = Permission.READ | Permission.WRITE
    print(f"  Permissions   : {user_perms}")
    print(f"  Can read      : {Permission.READ in user_perms}")
    print(f"  Can execute   : {Permission.EXECUTE in user_perms}")