from django.db.models.signals import post_save
from django.dispatch import receiver

from aploader.models import APElectionMeta
from election.models import Candidate, Election, CandidateElection
from electionnight.celery import (
    bake_state,
    bake_body,
    bake_state_body,
    bake_office,
)
from entity.models import Person
from vote.models import Votes


@receiver(post_save, sender=APElectionMeta)
@receiver(post_save, sender=Candidate)
@receiver(post_save, sender=Election)
@receiver(post_save, sender=CandidateElection)
@receiver(post_save, sender=Person)
@receiver(post_save, sender=Votes)
def rebake_context(sender, instance, **kwargs):
    if sender == APElectionMeta:
        office = instance.election.race.office

    if sender == Candidate:
        office = instance.race.office

    if sender == Election:
        office = instance.race.office

    if sender == CandidateElection:
        office = instance.election.race.office

    if sender == Person:
        candidacy = instance.candidacies.get(race__cycle__slug="2018")
        office = candidacy.race.office

    if sender == Votes:
        office = instance.candidate_election.election.race.office

    if office.body == "house":
        state = office.division.parent
    else:
        state = office.division

    bake_state.delay(state.code)
    if not office.body:
        bake_office.delay(state.code, office.slug)
    else:
        body = office.body
        bake_body.delay(body.slug)
        bake_state_body.delay(state.code, body.slug)
