from django.core.management import call_command
from django.core.management.base import BaseCommand

from vote.models import Votes


class Command(BaseCommand):
    help = 'Get an election ready to publish zeroes'

    def add_arguments(self, parser):
        parser.add_argument('election_date', type=str)
        parser.add_argument(
            '--test',
            dest='test',
            action='store_true',
        )

    def handle(self, *args, **options):
        Votes.objects.filter(
            candidate_election__election__election_day__slug=options['election_date']
        ).delete()

        call_command(
            'bootstrap_elex', options['election_date'], test=options['test']
        )

        call_command('bootstrap_results_config', options['election_date'])

        call_command('bootstrap_content', options['election_date'])

        call_command(
            'get_results',
            options['election_date'],
            test=options['test'],
            zeroes=True,
            run_once=True
        )