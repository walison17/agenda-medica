import pytest

from model_bakery import baker


@pytest.fixture
def paciente(django_user_model):
    return baker.make(django_user_model)


@pytest.fixture
def horario():
    return baker.make('core.AgendaHora', hora='9:00')


@pytest.fixture
def consulta(paciente, horario):
    agenda = horario.agenda

    return baker.make(
        'core.Consulta',
        paciente=paciente,
        medico=agenda.medico,
        dia=agenda.dia,
        horario=horario.hora
    )
