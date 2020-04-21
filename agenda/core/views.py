from rest_framework import generics, filters

from .models import Medico, Especialidade
from .serializers import MedicoSerializer, EspecialidadeSerializer


class EspecialidadeList(generics.ListAPIView):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']


class MedicoList(generics.ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
