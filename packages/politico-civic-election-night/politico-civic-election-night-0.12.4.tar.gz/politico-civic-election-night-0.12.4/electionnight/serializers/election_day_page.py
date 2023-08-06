from election.models import ElectionDay, Election
from geography.models import Division, DivisionLevel
from government.models import Party
from rest_framework import serializers
from rest_framework.reverse import reverse

from .division import DivisionSerializer
from .election import ElectionSerializer
from .party import PartySerializer


class ElectionDayPageListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse(
            "electionnight_api_election-day-detail",
            request=self.context["request"],
            kwargs={"pk": obj.pk},
        )

    class Meta:
        model = Division
        fields = ("url", "uid", "slug")


class ElectionDayPageSerializer(serializers.ModelSerializer):
    division = serializers.SerializerMethodField()
    parties = serializers.SerializerMethodField()
    elections = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_division(self, obj):
        us_object = Division.objects.get(level__name=DivisionLevel.COUNTRY)
        us = DivisionSerializer(us_object).data

        us["children"] = [
            DivisionSerializer(
                state,
                context={"children_level": DivisionLevel.DISTRICT},
            ).data
            for state in us_object.children.all()
        ]

        return us

    def get_parties(self, obj):
        return PartySerializer(Party.objects.all(), many=True).data

    def get_elections(self, obj):
        elections = Election.objects.filter(election_day=obj)
        return ElectionSerializer(elections, many=True).data

    def get_content(self, obj):
        pass

    class Meta:
        model = ElectionDay
        fields = ("uid", "content", "elections", "parties", "division")
