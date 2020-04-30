import pytest
from model_bakery import baker

from ..models import Medico
from ..filters import MedicoFilter

pytestmark = pytest.mark.django_db


@pytest.fixture
def especialidade_a():
    return baker.make('core.Especialidade', nome='a')


@pytest.fixture
def especialidade_b():
    return baker.make('core.Especialidade', nome='b')


@pytest.fixture
def medicos_a(especialidade_a):
    return baker.make(Medico, 2, especialidade=especialidade_a)


@pytest.fixture
def medicos_b(especialidade_b):
    return baker.make(Medico, 3, especialidade=especialidade_b)


def test_medico_filter_com_uma_especialidade(especialidade_a, medicos_a, medicos_b):
    f = MedicoFilter(
        {'especialidade': str(especialidade_a.pk)},
        queryset=Medico.objects.all()
    )

    assert all([m.especialidade.pk == especialidade_a.pk for m in f.qs])
    assert f.qs.count() == 2
    assert Medico.objects.count() == 5


def test_medico_filter_com_varias_especialidades(
    especialidade_a, especialidade_b, medicos_a, medicos_b
):
    f = MedicoFilter(
        {'especialidade[]': [str(especialidade_a.pk), str(especialidade_b.pk)]},
        queryset=Medico.objects.all()
    )

    assert f.qs.count() == 5
    assert Medico.objects.count() == 5
