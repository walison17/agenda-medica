from django.contrib import admin

from .models import (
    Agenda,
    AgendaHora,
    Consulta,
    Especialidade,
    Medico
)


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'crm', 'especialidade']
    list_filter = ['especialidade__nome']


class AgendaHoraInline(admin.StackedInline):
    model = AgendaHora


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ['medico', 'dia']
    inlines = [AgendaHoraInline]


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['dia', 'horario', 'paciente', 'medico']
    list_filter = ['dia', 'horario', 'paciente', 'medico']


admin.site.register(Especialidade)
