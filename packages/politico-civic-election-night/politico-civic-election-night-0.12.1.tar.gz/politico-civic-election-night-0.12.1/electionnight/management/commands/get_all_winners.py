import csv

from django.core.management.base import BaseCommand

from geography.models import DivisionLevel
from vote.models import Votes


class Command(BaseCommand):
    help = "Gets state-level House results"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        state_votes = Votes.objects.filter(
            division__level__slug="state", winning=True
        ).order_by(
            "division__label",
            "candidate_election__election__division__code",
            "candidate_election__candidate__party__label",
        )

        with open("test.csv", "w") as f:
            writer = csv.writer(f)
            header_row = [
                "State",
                "District",
                "Body",
                "First",
                "Last",
                "Party",
                "Incumbent",
            ]
            writer.writerow(header_row)

            for votes in state_votes:
                election = votes.candidate_election.election
                candidate = votes.candidate_election.candidate

                row = [
                    votes.division.label,
                    election.division.code
                    if election.division.level.name == DivisionLevel.DISTRICT
                    else None,
                    election.race.office.body.slug
                    if election.race.office.body
                    else "governor",
                    candidate.person.first_name,
                    candidate.person.last_name,
                    candidate.party.label,
                    candidate.incumbent,
                ]

                writer.writerow(row)
