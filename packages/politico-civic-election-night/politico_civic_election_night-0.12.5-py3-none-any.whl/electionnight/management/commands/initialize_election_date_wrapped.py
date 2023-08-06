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
        parser.add_argument(
            "--senate_class", dest="senate_class", action="store", default="1"
        )
        parser.add_argument("--test", dest="test", action="store_true")

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

        call_command("bootstrap_specials")
        call_command(
            "initialize_election_date",
            options["election_date"],
            test=options["test"],
        )

        for sender in senders:
            signal.connect(receiver=rebake_context, sender=sender)
