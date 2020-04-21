from rest_framework.generics import ListAPIView

from .models import Medico, Especialidade
from .serializers import MedicoSerializer, EspecialidadeSerializer


class EspecialidadeList(ListAPIView):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer


class MedicoList(ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
