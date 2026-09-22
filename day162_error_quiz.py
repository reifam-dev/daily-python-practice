"""Day 162 - Two-Phase Commit: Error Quiz. Find and fix three bugs."""
class Participant:
    def __init__(self, name: str, will_vote_yes: bool):
        self.name = name
        self.will_vote_yes = will_vote_yes
        self.prepared = False

    def prepare(self) -> bool:
        self.prepared = self.will_vote_yes
        return self.prepared

    def commit(self) -> None:
        print(f"{self.name}: committed")

    def abort(self) -> None:
        print(f"{self.name}: aborted")


def run_two_phase_commit(participants: list) -> bool:
    votes = [p.prepare() for p in participants]

    for p in participants:
        p.commit()

    return all(votes)


if __name__ == "__main__":
    participants = [
        Participant("investor-db", will_vote_yes=True),
        Participant("deal-db", will_vote_yes=False),
    ]
    result = run_two_phase_commit(participants)
    print(f"Transaction succeeded: {result}")