from datetime import date

from django.db import models
from django.db.models import (
    Prefetch, OuterRef, Subquery, Exists,
)


class AgendaQuerySet(models.QuerySet):
    def prefetch_horarios_disponiveis(self):
        from .models import AgendaHora

        horarios_disponiveis = (
            AgendaHora
            .objects
            .filter(disponivel=True)
        )

        return self.prefetch_related(
            Prefetch('horarios', queryset=horarios_disponiveis, to_attr='horarios_disponiveis')
        )


class AgendaDisponivelManager(models.Manager):
    def get_queryset(self):
        from .models import AgendaHora

        horarios = (
            AgendaHora
            .objects
            .filter(agenda=OuterRef('pk'), disponivel=True)
        )

        return super().get_queryset().filter(dia__gte=date.today()).filter(Exists(horarios))
