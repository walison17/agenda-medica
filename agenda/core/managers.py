from django.db import models
from django.db.models import Case, Exists, OuterRef, Prefetch, Q, Value, When
from django.utils import timezone


class AgendaQuerySet(models.QuerySet):
    def carregar_apenas_horarios_disponiveis(self):
        from .models import AgendaHora

        agora = timezone.now()
        hoje = agora.date()
        hora = agora.strftime('%H:%M')

        horarios_disponiveis = (
            AgendaHora
            .disponiveis
            .filter(
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

        agora = timezone.now()
        hoje = agora.date()
        hora = agora.strftime('%H:%M')

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

        qs = super().get_queryset()
        return qs.filter(dia__gte=hoje).filter(Exists(horarios_disponiveis))
