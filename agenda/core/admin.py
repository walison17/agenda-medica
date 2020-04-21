from django.contrib import admin

from .models import Medico, Especialidade, Agenda, AgendaHora


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


admin.site.register(Especialidade)
