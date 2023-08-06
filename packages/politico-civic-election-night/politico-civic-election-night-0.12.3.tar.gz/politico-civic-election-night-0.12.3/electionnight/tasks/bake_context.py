import logging

from celery import shared_task
from geography.models import Division, DivisionLevel
from government.models import Body, Office
from rest_framework.renderers import JSONRenderer

from electionnight.serializers import (
    BodySerializer,
    OfficeSerializer,
    StateSerializer,
)
from electionnight.utils.aws import defaults, get_bucket

logger = logging.getLogger("tasks")


@shared_task(acks_late=True)
def bake_state(code):
    state = Division.objects.get(code=code, level__name=DivisionLevel.STATE)
    print("Baking {} context data".format(state.label))
    data = StateSerializer(state, context={"election_date": "2018-11-06"}).data
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


@shared_task(acks_late=True)
def bake_body(slug):
    body = Body.objects.get(slug=slug)
    print("Baking {} context data".format(body.label))
    data = BodySerializer(body, context={"election_date": "2018-11-06"}).data
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


@shared_task(acks_late=True)
def bake_state_body(code, slug):
    state = Division.objects.get(code=code, level__name=DivisionLevel.STATE)
    body = Body.objects.get(slug=slug)
    print("Baking {} {} context data".format(state.label, body.label))
    data = BodySerializer(
        body, context={"election_date": "2018-11-06", "division": state}
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


@shared_task(acks_late=True)
def bake_office(code, slug):
    state = Division.objects.get(code=code, level__name=DivisionLevel.STATE)
    office = Office.objects.get(division=state, slug=slug)
    print("Baking {} {} context data".format(state.label, office.label))
    data = OfficeSerializer(
        office, context={"election_date": "2018-11-06"}
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
