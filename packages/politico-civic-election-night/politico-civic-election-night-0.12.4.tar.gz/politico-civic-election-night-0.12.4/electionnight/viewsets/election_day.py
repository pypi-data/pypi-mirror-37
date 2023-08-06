from election.models import ElectionDay
from electionnight.serializers import (
    ElectionDaySerializer,
    ElectionDayPageSerializer,
    ElectionDayPageListSerializer
)

from rest_framework import generics


class ElectionDayList(generics.ListAPIView):
    serializer_class = ElectionDaySerializer
    queryset = ElectionDay.objects.all()


class ElectionDayDetail(generics.RetrieveAPIView):
    serializer_class = ElectionDaySerializer
    queryset = ElectionDay.objects.all()


class ElectionDayPageList(generics.ListAPIView):
    serializer_class = ElectionDayPageListSerializer
    queryset = ElectionDay.objects.all()


class ElectionDayPageDetail(generics.RetrieveAPIView):
    serializer_class = ElectionDayPageSerializer
    queryset = ElectionDay.objects.all()