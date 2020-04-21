from django.urls import path

from rest_framework import routers

from .views import (
    EspecialidadeList,
    MedicoList,
    AgendaList,
    ConsultaViewSet
)

router = routers.SimpleRouter()
router.register(r'consultas', ConsultaViewSet, basename='consulta')

urlpatterns = [
    path('agendas/', AgendaList.as_view()),
    path('especialidades/', EspecialidadeList.as_view()),
    path('medicos/', MedicoList.as_view()),
]
urlpatterns += router.urls
