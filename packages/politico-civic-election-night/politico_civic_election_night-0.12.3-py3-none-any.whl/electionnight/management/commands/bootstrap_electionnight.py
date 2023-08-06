from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import signals

from election.models import Election
from electionnight.managers import TempDisconnectSignal
from electionnight.signals import rebake_context


class Command(BaseCommand):
    help = "Bootstrap development."

    def handle(self, *args, **options):
        call_command("bootstrap_geography")
        call_command("bootstrap_jurisdictions")
        call_command("bootstrap_fed")
        call_command("bootstrap_offices")
        call_command("bootstrap_parties")
        call_command("bootstrap_election_events")

        with TempDisconnectSignal(
            signal=signals.post_save, receiver=rebake_context, sender=Election
        ):
            call_command("bootstrap_elections")
