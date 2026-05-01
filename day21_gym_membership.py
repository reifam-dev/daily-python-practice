# Day 21 - Clean GymMembership class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class GymMembership:
    """Manages gym memberships with add, cancel and status checking."""

    def __init__(self) -> None:
        self._members: List[str] = []

    def add_member(self, name: str) -> None:
        """Add a new member. Raises ValueError if already a member or name invalid."""
        if not name or not name.strip():
            raise ValueError("Member name cannot be empty.")
        if name.strip() in self._members:
            raise ValueError(f"'{name}' is already a member.")
        self._members.append(name.strip())

    def cancel_membership(self, name: str) -> None:
        """Cancel a membership. Raises KeyError if member not found."""
        if name not in self._members:
            raise KeyError(f"'{name}' is not a current member.")
        self._members.remove(name)

    def is_active(self, name: str) -> bool:
        """Return True if the person is an active member."""
        return name in self._members

    def get_member_count(self) -> int:
        """Return the total number of active members."""
        return len(self._members)

    def get_all_members(self) -> List[str]:
        """Return a copy of all active members."""
        return self._members.copy()


if __name__ == "__main__":
    try:
        gym = GymMembership()
        gym.add_member("Alice")
        gym.add_member("Bob")
        gym.add_member("Charlie")

        print(f"Members       : {gym.get_all_members()}")
        print(f"Total         : {gym.get_member_count()}")
        print(f"Alice active  : {gym.is_active('Alice')}")
        print(f"Dave active   : {gym.is_active('Dave')}")

        gym.cancel_membership("Bob")
        print(f"After cancelling Bob: {gym.get_all_members()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")