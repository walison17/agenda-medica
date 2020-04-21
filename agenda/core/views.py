from rest_framework import generics, filters

from django_filters.rest_framework import DjangoFilterBackend

from .models import Medico, Especialidade, Agenda
from .serializers import MedicoSerializer, EspecialidadeSerializer, AgendaSerializer
from .filters import MedicoFilter


class EspecialidadeList(generics.ListAPIView):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']


class MedicoList(generics.ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    search_fields = ['nome']
    filterset_class = MedicoFilter


class AgendaList(generics.ListAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
