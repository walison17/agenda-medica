from datetime import date

from django.db import models
from django.core.exceptions import ValidationError


class Especialidade(models.Model):
    nome = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome.title()


class Medico(models.Model):
    nome = models.CharField(max_length=128)
    crm = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=11, blank=True)
    especialidade = models.ForeignKey(
        Especialidade, related_name='medicos', on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


def validate_date(value):
    if value < date.today():
        raise ValidationError('Não é possível criar uma agenda para uma data retroativa.')


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, related_name='agendas', on_delete=models.PROTECT)
    dia = models.DateField(validators=[validate_date])

    class Meta:
        ordering = ['dia']
        unique_together = ['medico', 'dia']

    def __str__(self):
        return f'médico: {self.medico}, data: {self.dia}'


class AgendaHora(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.PROTECT)
    hora = models.TimeField()

    class Meta:
        verbose_name = 'Horário'
        ordering = ['hora']
        unique_together = ['agenda', 'hora']

    def __str__(self):
        return self.hora.strftime('%H:%M')