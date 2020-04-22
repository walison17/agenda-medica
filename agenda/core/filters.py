import django_filters
from django_filters import widgets

from .models import Medico, Especialidade, Agenda


class MedicoFilter(django_filters.FilterSet):
    especialidade = django_filters.ModelMultipleChoiceFilter(
        queryset=Especialidade.objects.all(),
        widget=widgets.QueryArrayWidget()
    )

    class Meta:
        model = Medico
        fields = ['especialidade']


class AgendaFilter(django_filters.FilterSet):
    medico = django_filters.ModelMultipleChoiceFilter(
        queryset=Medico.objects.all(),
        field_name='medico',
        label='médico',
        widget=widgets.QueryArrayWidget()
    )
    especialidade = django_filters.ModelMultipleChoiceFilter(
        queryset=Especialidade.objects.all(),
        field_name='medico__especialidade',
        label='especialidade',
        widget=widgets.QueryArrayWidget()
    )
    data_inicio = django_filters.DateFilter(field_name='dia', lookup_expr='gte')
    data_final = django_filters.DateFilter(field_name='dia', lookup_expr='lte')

    class Meta:
        model = Agenda
        fields = [
            'medico',
            'especialidade',
            'data_inicio',
            'data_final'
        ]
