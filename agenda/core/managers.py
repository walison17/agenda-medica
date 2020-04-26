from django.db import models
from django.utils import timezone
from django.db.models import (
    Prefetch, OuterRef, Exists, Case, When, Value, Q
)


class AgendaQuerySet(models.QuerySet):
    def carregar_apenas_horarios_disponiveis(self):
        from .models import AgendaHora

        hoje = timezone.localdate()
        hora = timezone.now().strftime('%H:%M')

        horarios_disponiveis = (
            AgendaHora
            .disponiveis
            .filter(
                disponivel=True,
                hora__gte=Case(
                    When(
                        Q(agenda__dia=hoje), then=Value(hora)
                    ),
                    default=Value('00:00')
                )
            )
        )

        return self.prefetch_related(
            Prefetch('horarios', queryset=horarios_disponiveis, to_attr='horarios_disponiveis')
        )


class AgendaDisponivelManager(models.Manager):
    def get_queryset(self):
        from .models import AgendaHora

        hoje = timezone.localdate()
        hora = timezone.now().strftime('%H:%M')

        horarios_disponiveis = (
            AgendaHora
            .disponiveis
            .filter(
                agenda=OuterRef('pk'),
                hora__gte=Case(
                    When(
                        Q(agenda__dia=hoje), then=Value(hora)
                    ),
                    default=Value('00:00')
                )
            )
        )

        qs = AgendaQuerySet(self.model, using=self._db)
        return qs.filter(dia__gte=hoje).filter(Exists(horarios_disponiveis))
