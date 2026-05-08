# Day 29 - Error Finding Quiz

class SportsTeam:

    def __init__(self, team_name, max_players):
        self.team_name = team_name
        self.max_players = max_players
        self.squad = []

    def add_player(self, name):
        if len(self.squad) >= self.max_players:
            print("Squad is full.")
        squad.append(name)             # Bug 1 - missing self, missing else

    def remove_player(self, name):
        self.squad.remove(name)        # Bug 2 - no check

    def is_in_squad(self, name):
        return name in self.squad

    def get_squad_size(self):
        return len(squad)              # Bug 3 - missing self

team = SportsTeam("Eagles", 5)
team.add_player("Alice")
team.add_player("Bob")
print(team.is_in_squad("Alice"))
print(team.get_squad_size())