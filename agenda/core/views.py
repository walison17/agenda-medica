from rest_framework import generics, filters, mixins, viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .models import Medico, Especialidade, Agenda, Consulta
from .serializers import (
    MedicoSerializer,
    EspecialidadeSerializer,
    AgendaSerializer,
    ConsultaSerializer
)
from .filters import MedicoFilter, AgendaFilter


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
    queryset = Agenda.disponiveis.carregar_apenas_horarios_disponiveis()
    serializer_class = AgendaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AgendaFilter


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class ConsultaViewSet(CreateListDestroyViewSet):
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        return Consulta.objects.filter(paciente=self.request.user)
