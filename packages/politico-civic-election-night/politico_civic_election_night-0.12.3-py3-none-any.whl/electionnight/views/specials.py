"""
Special election result pages.

URL PATTERNS:
/election-results/{YEAR}/{STATE}/special-election/{MMM}-{DD}/
"""
import json

from datetime import datetime, timedelta
from time import strptime

from almanac.models import ElectionEvent
from django.shortcuts import get_object_or_404
from django.urls import reverse
from election.models import ElectionDay, Election
from electionnight.conf import settings
from electionnight.models import PageContent
from electionnight.serializers import ElectionViewSerializer, StateSerializer
from geography.models import Division, DivisionLevel

from .base import BaseView


class SpecialElectionPage(BaseView):
    """
    **Preview URL**: :code:`/state/{YEAR}/{STATE}/{ELECTION_DATE}/`
    """
    name = 'electionnight_special-election-page'
    path = (
        r'^special/(?P<year>\d{4})/(?P<state>[\w-]+)/special-election/'
        r'(?P<month>\w{3})-(?P<day>\d{2})/$'
    )

    js_dev_path = 'electionnight/js/main-special-app.js'
    css_dev_path = 'electionnight/css/main-special-app.css'

    model = Division
    context_object_name = 'division'
    template_name = 'electionnight/specials/index.html'

    def get_queryset(self):
        level = DivisionLevel.objects.get(name=DivisionLevel.STATE)
        return self.model.objects.filter(level=level)

    def get_object(self, **kwargs):
        return get_object_or_404(Division, slug=self.kwargs.get('state'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Set kwargs to properties on class.
        self.division = context['division']
        self.year = self.kwargs.get('year')
        self.month = self.kwargs.get('month')
        self.day = self.kwargs.get('day')
        self.state = self.kwargs.get('state')
        self.election_date = '{}-{}-{}'.format(
            self.year,
            '{0:02d}'.format(strptime(self.month, '%b').tm_mon),
            self.day,
        )
        self.election = ElectionDay.objects.get(
            date=self.election_date,
        ).elections.get(
            race__special=True,
            division__parent__label=self.division
        )
        context['secret'] = settings.SECRET_KEY
        context['year'] = self.year
        context['month'] = self.month
        context['day'] = self.day
        context['state'] = self.state

        context['election_date'] = self.election_date
        context['coverage_end'] = (datetime.strptime(
            self.election_date, '%Y-%m-%d'
        ) + timedelta(days=2)).isoformat()

        context['content'] = PageContent.objects.division_content(
            ElectionDay.objects.get(date=self.election_date),
            self.division,
            special=True
        )
        # context['baked_content'] = context['content']['page']['before-results']
        context['election'] = self.election
        context['subpath'] = '/special-election/{}-{}'.format(
            self.month, self.day
        )

        template = {
            **context,
            **self.get_paths_context(production=context['production']),
            **self.get_elections_context(context['division']),
        }

        nav, nav_json = self.get_nav_links(context['subpath'])
        template['nav'] = nav
        template['nav_json'] = nav_json

        return template

    def get_nav_links(self, subpath=''):
        todays_elections = ElectionEvent.objects.filter(
            election_day__date=self.election_date,
            event_type__in=[ElectionEvent.PRIMARIES, ElectionEvent.GENERAL]
        ).values_list('division__label', flat=True)

        todays_runoffs = ElectionEvent.objects.filter(
            election_day__date=self.election_date,
            event_type__in=[
                ElectionEvent.PRIMARIES_RUNOFF, ElectionEvent.GENERAL_RUNOFF
            ]
        ).values_list('division__label', flat=True)

        specials = Election.objects.filter(
            election_day__date=self.election_date,
            race__special=True
        ).values_list('division__parent__label', flat=True)

        todays_specials = [state for state in specials if state not in todays_elections or todays_runoffs] # noqa

        state_level = DivisionLevel.objects.get(name=DivisionLevel.STATE)
        # All states except DC
        states = Division.objects.filter(
            level=state_level,
        ).exclude(code='11').order_by('label')
        # Nav links should always refer to main state page. We can use subpath
        # to determine how deep publish path is relative to state pages.
        relative_prefix = ''
        print(subpath)
        depth = subpath.lstrip('/').count('/')
        print(depth)
        for i in range(depth):
            relative_prefix += '../'
        data = {
            'states': [
                {
                    'link': '../../{0}{1}/'.format(
                        relative_prefix,
                        state.slug
                    ),
                    'name': state.label,
                    'live': state.label in todays_elections,
                    'runoff': state.label in todays_runoffs,
                    'special': state.label in todays_specials
                } for state in states
            ],
        }

        return data, json.dumps(data)

    def get_elections_context(self, division):
        elections_context = {}

        election_day = ElectionDay.objects.get(date=self.election_date)

        governor_elections = list(division.elections.filter(
            election_day=election_day,
            race__office__slug__contains='governor'
        ))
        senate_elections = list(division.elections.filter(
            election_day=election_day,
            race__office__body__slug__contains='senate'
        ))

        house_elections = {}
        district = DivisionLevel.objects.get(name=DivisionLevel.DISTRICT)
        for district in division.children.filter(
            level=district
        ).order_by('code'):
            district_elections = list(district.elections.filter(
                election_day=election_day
            ))
            serialized = ElectionViewSerializer(
                district_elections, many=True
            ).data

            if serialized == []:
                continue

            house_elections[district.label] = serialized

        elections_context['governor_elections'] = ElectionViewSerializer(
            governor_elections, many=True
        ).data

        elections_context['senate_elections'] = ElectionViewSerializer(
            senate_elections, many=True
        ).data

        elections_context['house_elections'] = house_elections

        return elections_context

    def get_publish_path(self):
        return 'election-results/{}/{}/special-election/{}-{}/'.format(
            self.year,
            self.state,
            self.month,
            self.day,
        )

    def get_serialized_context(self):
        """Get serialized context for baking to S3."""
        division = Division.objects.get(slug=self.state)
        return StateSerializer(division, context={
            'election_date': self.election_date,
            'special': True
        }).data

    def get_extra_static_paths(self, production):
        division = Division.objects.get(slug=self.state)
        geo = (
            'election-results/cdn/geography/us-census/cb/500k/2016/states/{0}/{0}'
        ).format(division.code)
        if (production and
           settings.AWS_S3_BUCKET == 'interactives.politico.com'):
            return {
                'context': 'context.json',
                'geo_county': (
                    'https://www.politico.com/'
                    '{}-county.json').format(geo),
                'geo_district': (
                    'https://www.politico.com/'
                    '/{}-district.json').format(geo),
            }
        elif (production and
              settings.AWS_S3_BUCKET != 'interactives.politico.com'):
            return {
                'context': 'context.json',
                'geo_county': (
                    'https://s3.amazonaws.com/'
                    'interactives.politico.com/{}-county.json').format(geo),
                'geo_district': (
                    'https://s3.amazonaws.com/'
                    'interactives.politico.com/{}-district.json').format(geo),
            }
        print(self.election)
        return {
            'context': reverse(
                'electionnight_api_special-election-detail',
                args=[self.election_date, self.election.division.pk],
            ),
            'geo_county': (
                'https://s3.amazonaws.com/'
                'interactives.politico.com/{}-county.json').format(geo),
            'geo_district': (
                'https://s3.amazonaws.com/'
                'interactives.politico.com/{}-district.json').format(geo),
        }
