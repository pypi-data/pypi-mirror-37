from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Publish zeroes for an election date'

    def add_arguments(self, parser):
        parser.add_argument('election_date', type=str)
        parser.add_argument(
            '--test',
            dest='test',
            action='store_true',
        )

    def handle(self, *args, **options):
        call_command('bake_elections', options['election_date'])

        call_command(
            'get_results',
            options['election_date'],
            test=options['test'],
            zeroes=True,
            run_once=True
        )
