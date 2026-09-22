"""Day 162 - Two-Phase Commit: phase 1 (prepare/vote) must fully
complete and be unanimous before phase 2 (commit) begins on anyone;
a single "no" vote aborts the whole transaction across every
participant, not just the one that voted no - PCPP1 standard."""
from __future__ import annotations


class Participant:
    def __init__(self, name: str, will_vote_yes: bool) -> None:
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


def run_two_phase_commit(participants: list[Participant]) -> bool:
    votes = [p.prepare() for p in participants]
    all_yes = all(votes)

    if all_yes:
        for p in participants:
            p.commit()
    else:
        for p in participants:
            p.abort()

    return all_yes


if __name__ == "__main__":
    participants = [
        Participant("investor-db", will_vote_yes=True),
        Participant("deal-db", will_vote_yes=False),
    ]
    result = run_two_phase_commit(participants)
    print(f"Transaction succeeded: {result}")  # False - both abort