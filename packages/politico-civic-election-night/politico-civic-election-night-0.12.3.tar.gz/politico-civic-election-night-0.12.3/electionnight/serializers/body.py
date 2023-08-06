from election.models import Election, ElectionDay
from geography.models import Division, DivisionLevel
from government.models import Body, Party
from rest_framework import serializers
from rest_framework.reverse import reverse

from electionnight.models import PageContent

from .division import DivisionSerializer
from .election import ElectionSerializer
from .party import PartySerializer


class BodyListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse(
            "electionnight_api_body-election-detail",
            request=self.context["request"],
            kwargs={"pk": obj.pk, "date": self.context["election_date"]},
        )

    class Meta:
        model = Division
        fields = ("url", "uid", "slug")


class BodySerializer(serializers.ModelSerializer):
    division = serializers.SerializerMethodField()
    parties = serializers.SerializerMethodField()
    elections = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_division(self, obj):
        """Division."""
        if self.context.get("division"):
            return DivisionSerializer(self.context.get("division")).data
        else:
            if obj.slug == "senate":
                return DivisionSerializer(obj.jurisdiction.division).data
            else:
                us = DivisionSerializer(obj.jurisdiction.division).data

                us["children"] = [
                    DivisionSerializer(
                        state,
                        context={"children_level": DivisionLevel.DISTRICT},
                    ).data
                    for state in obj.jurisdiction.division.children.all()
                ]

                return us

    def get_parties(self, obj):
        """All parties."""
        return PartySerializer(Party.objects.all(), many=True).data

    def get_elections(self, obj):
        """All elections held on an election day."""
        election_day = ElectionDay.objects.get(
            date=self.context["election_date"]
        )

        kwargs = {"race__office__body": obj, "election_day": election_day}
        if self.context.get("division") and obj.slug == "senate":
            kwargs["division"] = self.context["division"]
        elif self.context.get("division") and obj.slug == "house":
            kwargs["division__parent"] = self.context["division"]

        if obj.slug == "house" and not self.context.get("division"):
            kwargs["race__special"] = False

        elections = Election.objects.filter(**kwargs)
        return ElectionSerializer(elections, many=True).data

    def get_content(self, obj):
        """All content for body's page on an election day."""
        election_day = ElectionDay.objects.get(
            date=self.context["election_date"]
        )
        return PageContent.objects.body_content(election_day, obj)

    class Meta:
        model = Body
        fields = ("uid", "content", "elections", "parties", "division")
