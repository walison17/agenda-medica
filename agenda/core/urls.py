from django.urls import path

from .views import EspecialidadeList, MedicoList, AgendaList

urlpatterns = [
    path('agendas/', AgendaList.as_view()),
    path('especialidades/', EspecialidadeList.as_view()),
    path('medicos/', MedicoList.as_view()),
]
