# Day 29 - Clean SportsTeam class (PEP 8, docstrings, type hints, exceptions)

from typing import List


class SportsTeam:
    """Manages a sports team squad with a name and maximum player limit."""

    def __init__(self, team_name: str, max_players: int) -> None:
        if not team_name or not team_name.strip():
            raise ValueError("Team name cannot be empty.")
        if max_players <= 0:
            raise ValueError("Max players must be a positive integer.")
        self._team_name: str = team_name.strip()
        self._max_players: int = max_players
        self._squad: List[str] = []

    def add_player(self, name: str) -> None:
        """Add a player to the squad. Raises ValueError if full, duplicate or name invalid."""
        if not name or not name.strip():
            raise ValueError("Player name cannot be empty.")
        if name.strip() in self._squad:
            raise ValueError(f"'{name}' is already in the squad.")
        if len(self._squad) >= self._max_players:
            raise ValueError(f"Squad is full. Maximum players: {self._max_players}.")
        self._squad.append(name.strip())

    def remove_player(self, name: str) -> None:
        """Remove a player from the squad. Raises KeyError if not found."""
        if name not in self._squad:
            raise KeyError(f"'{name}' is not in the squad.")
        self._squad.remove(name)

    def is_in_squad(self, name: str) -> bool:
        """Return True if the player is in the squad."""
        return name in self._squad

    def get_squad_size(self) -> int:
        """Return the current number of players in the squad."""
        return len(self._squad)

    def get_team_name(self) -> str:
        """Return the team name."""
        return self._team_name

    def get_all_players(self) -> List[str]:
        """Return a copy of all players in the squad."""
        return self._squad.copy()


if __name__ == "__main__":
    try:
        team = SportsTeam("Eagles", 5)
        team.add_player("Alice")
        team.add_player("Bob")
        team.add_player("Charlie")

        print(f"Team             : {team.get_team_name()}")
        print(f"Squad            : {team.get_all_players()}")
        print(f"Squad size       : {team.get_squad_size()}")
        print(f"Alice in squad   : {team.is_in_squad('Alice')}")
        print(f"Dave in squad    : {team.is_in_squad('Dave')}")

        team.remove_player("Bob")
        print(f"After removing Bob: {team.get_all_players()}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")