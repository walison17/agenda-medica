from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from model_utils.managers import QueryManager

from .managers import AgendaDisponivelManager, AgendaQuerySet


class Especialidade(models.Model):
    nome = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome.title()


class Medico(models.Model):
    nome = models.CharField(max_length=128)
    crm = models.IntegerField(unique=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=11, blank=True)
    especialidade = models.ForeignKey(
        Especialidade, related_name='medicos', on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Consulta(models.Model):
    dia = models.DateField()
    horario = models.TimeField('horário')
    data_agendamento = models.DateTimeField('data do agendamento', auto_now_add=True)
    medico = models.ForeignKey(
        Medico,
        related_name='consultas',
        on_delete=models.PROTECT
    )
    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='consultas',
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['dia', 'horario']
        unique_together = ['dia', 'horario', 'paciente']

    def __str__(self):
        return (
            f"médico: {self.medico}, dia: {self.dia.strftime('%d/%m/%Y')} "
            f"às {self.horario.strftime('%H:%M')}"
        )


def validate_date(value):
    if value < date.today():
        raise ValidationError('Não é possível criar uma agenda para uma data retroativa.')


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, related_name='agendas', on_delete=models.PROTECT)
    dia = models.DateField(validators=[validate_date])

    objects = models.Manager()
    disponiveis = AgendaDisponivelManager.from_queryset(AgendaQuerySet)()

    class Meta:
        ordering = ['dia']
        unique_together = ['medico', 'dia']

    def __str__(self):
        return f'{self.medico} - {self.dia.strftime("%d/%m/%Y")}'


class AgendaHora(models.Model):
    agenda = models.ForeignKey(Agenda, related_name='horarios', on_delete=models.PROTECT)
    hora = models.TimeField()
    disponivel = models.BooleanField('disponível', default=True, editable=False)

    objects = models.Manager()
    disponiveis = QueryManager(disponivel=True)

    class Meta:
        verbose_name = 'Horário'
        ordering = ['hora']
        unique_together = ['agenda', 'hora']

    def __str__(self):
        return self.hora.strftime('%H:%M')


@receiver(post_save, sender=Consulta)
def marcar_horario_como_indisponivel(sender, instance, created, **kwargs):
    if created:
        (
            AgendaHora
            .objects
            .filter(agenda__medico=instance.medico, agenda__dia=instance.dia, hora=instance.horario)
            .update(disponivel=False)
        )


@receiver(post_delete, sender=Consulta)
def marcar_horario_como_disponivel(sender, instance, **kwargs):
    (
        AgendaHora
        .objects
        .filter(agenda__medico=instance.medico, agenda__dia=instance.dia, hora=instance.horario)
        .update(disponivel=True)
    )
