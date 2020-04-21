from django.urls import path

from .views import EspecialidadeList, MedicoList

urlpatterns = [
    path('especialidades/', EspecialidadeList.as_view()),
    path('medicos/', MedicoList.as_view()),
]
