from datetime import date

from django.db import models
from django.db.models import (
    Prefetch, OuterRef, Subquery, Exists,
)


class AgendaQuerySet(models.QuerySet):
    def prefetch_horarios_disponiveis(self):
        from .models import Consulta, AgendaHora

        consultas = (
            Consulta
            .objects
            .filter(
                dia=OuterRef('agenda__dia'),
                medico=OuterRef('agenda__medico')
            )
            .values('horario')
        )
        horarios = (
            AgendaHora
            .objects
            .exclude(hora__in=Subquery(consultas))
        )

        return self.prefetch_related(
            Prefetch('horarios', queryset=horarios, to_attr='horarios_disponiveis')
        )


class AgendaDisponivelManager(models.Manager):
    def get_queryset(self):
        from .models import Consulta, AgendaHora

        consultas = (
            Consulta
            .objects
            .filter(
                dia=OuterRef('agenda__dia'),
                medico=OuterRef('agenda__medico')
            )
            .values('horario')
        )
        horarios = (
            AgendaHora
            .objects
            .filter(agenda=OuterRef('pk'))
            .exclude(hora__in=Subquery(consultas))
        )

        return super().get_queryset().filter(dia__gte=date.today()).filter(Exists(horarios))
