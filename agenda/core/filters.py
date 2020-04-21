import django_filters
from django_filters import widgets

from .models import Medico, Especialidade


class MedicoFilter(django_filters.FilterSet):
    especialidade = django_filters.ModelMultipleChoiceFilter(
        queryset=Especialidade.objects.all(),
        widget=widgets.QueryArrayWidget()
    )

    class Meta:
        model = Medico
        fields = ['especialidade']
