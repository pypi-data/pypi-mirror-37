from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import signals

from aploader.models import APElectionMeta
from election.models import Candidate, Election, CandidateElection
from entity.models import Person
from vote.models import Votes
from electionnight.signals import rebake_context


class Command(BaseCommand):
    help = "Bootstrap development."

    def add_arguments(self, parser):
        parser.add_argument("election_date", type=str)
        parser.add_argument("level", type=str)
        parser.add_argument("--run_once", dest="run_once", action="store_true")
        parser.add_argument(
            "--tabulated", dest="tabulated", action="store_true"
        )
        parser.add_argument("--nobots", dest="no_bots", action="store_true")

    def handle(self, *args, **options):
        signal = signals.post_save

        senders = [
            APElectionMeta,
            Candidate,
            Election,
            CandidateElection,
            Person,
            Votes,
        ]
        for sender in senders:
            signal.disconnect(receiver=rebake_context, sender=sender)

        call_command(
            "reup_to_db",
            options["election_date"],
            options["level"],
            run_once=options["run_once"],
            tabulated=options["tabulated"],
            no_bots=options["no_bots"],
        )

        for sender in senders:
            signal.connect(receiver=rebake_context, sender=sender)
