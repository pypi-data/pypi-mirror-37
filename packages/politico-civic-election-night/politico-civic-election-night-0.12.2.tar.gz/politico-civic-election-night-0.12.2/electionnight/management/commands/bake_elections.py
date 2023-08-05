from django.core.management.base import BaseCommand
from election.models import ElectionDay
from geography.models import DivisionLevel
from rest_framework.renderers import JSONRenderer
from tqdm import tqdm

from electionnight.serializers import (
    BodySerializer,
    OfficeSerializer,
    StateSerializer,
)
from electionnight.utils.aws import defaults, get_bucket


# TODO: Clean this up and split methods out...
class Command(BaseCommand):
    help = "Publishes an election!"

    def add_arguments(self, parser):
        parser.add_argument(
            "election_dates", nargs="+", help="Election dates to publish."
        )

    def fetch_states(self, elections):
        """
        Returns the unique divisions for all elections on an election day.
        """
        states = []

        for election in elections:
            if election.division.level.name == DivisionLevel.DISTRICT:
                division = election.division.parent
            else:
                division = election.division

            states.append(division)

        return sorted(list(set(states)), key=lambda s: s.label)

    def fetch_bodies(self, elections):
        bodies = []

        for election in elections:
            if election.race.office.body:
                bodies.append(election.race.office.body)

        return sorted(list(set(bodies)), key=lambda b: b.label)

    def fetch_executive_offices(self, elections):
        offices = []

        for election in elections:
            if election.race.office.is_executive:
                offices.append(election.race.office)

        return list(set(offices))

    def bake_states(self, elections):
        states = self.fetch_states(elections)
        self.stdout.write(self.style.SUCCESS("Baking state page data."))
        for state in tqdm(states):
            self.stdout.write("> {}".format(state.name))
            data = StateSerializer(
                state, context={"election_date": self.ELECTION_DAY.slug}
            ).data
            json_string = JSONRenderer().render(data)
            key = "election-results/2018/{}/context.json".format(state.slug)
            bucket = get_bucket()
            bucket.put_object(
                Key=key,
                ACL=defaults.ACL,
                Body=json_string,
                CacheControl=defaults.CACHE_HEADER,
                ContentType="application/json",
            )

    def bake_bodies(self, elections):
        bodies = self.fetch_bodies(elections)
        self.stdout.write(self.style.SUCCESS("Baking body page data."))
        for body in tqdm(bodies):
            self.stdout.write("> {}".format(body.label))
            data = BodySerializer(
                body, context={"election_date": self.ELECTION_DAY.slug}
            ).data
            json_string = JSONRenderer().render(data)
            key = "election-results/2018/{}/context.json".format(body.slug)
            bucket = get_bucket()
            bucket.put_object(
                Key=key,
                ACL=defaults.ACL,
                Body=json_string,
                CacheControl=defaults.CACHE_HEADER,
                ContentType="application/json",
            )

    def bake_state_bodies(self, elections):
        self.stdout.write(self.style.SUCCESS("Baking state body page data."))
        states = self.fetch_states(elections)
        for state in tqdm(states, desc="States"):
            state_elections = elections.filter(division=state)
            house_elections = elections.filter(division__parent=state)
            state_elections = list(state_elections) + list(house_elections)
            bodies = self.fetch_bodies(state_elections)
            for body in tqdm(bodies, desc="Bodies", leave=False):
                tqdm.write("{} {}".format(state.label, body.label))
                data = BodySerializer(
                    body,
                    context={
                        "election_date": self.ELECTION_DAY.slug,
                        "division": state,
                    },
                ).data
                json_string = JSONRenderer().render(data)
                key = "election-results/2018/{}/{}/context.json".format(
                    state.slug, body.slug
                )
                bucket = get_bucket()
                bucket.put_object(
                    Key=key,
                    ACL=defaults.ACL,
                    Body=json_string,
                    CacheControl=defaults.CACHE_HEADER,
                    ContentType="application/json",
                )

    def bake_state_executive_offices(self, elections):
        self.stdout.write(self.style.SUCCESS("Baking state office page data."))
        states = self.fetch_states(elections)
        for state in tqdm(states, desc="States"):
            state_elections = elections.filter(division=state)
            offices = self.fetch_executive_offices(state_elections)
            for office in tqdm(offices, desc="Offices", leave=False):
                tqdm.write(office.label)
                data = OfficeSerializer(
                    office, context={"election_date": self.ELECTION_DAY.slug}
                ).data
                json_string = JSONRenderer().render(data)
                key = "election-results/2018/{}/{}/context.json".format(
                    state.slug, office.slug.split("-")[-1]
                )
                bucket = get_bucket()
                bucket.put_object(
                    Key=key,
                    ACL=defaults.ACL,
                    Body=json_string,
                    CacheControl=defaults.CACHE_HEADER,
                    ContentType="application/json",
                )

    def handle(self, *args, **options):
        election_dates = options["election_dates"]
        for date in election_dates:
            election_day = ElectionDay.objects.get(date=date)
            self.ELECTION_DAY = election_day
            elections = election_day.elections.all()
            self.bake_states(elections)
            self.bake_bodies(elections)
            self.bake_state_bodies(elections)
            self.bake_state_executive_offices(elections)
