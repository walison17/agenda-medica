import pytest

from model_bakery import baker
from rest_framework.test import APIClient, force_authenticate

from agenda.core.models import Consulta

from ..models import Consulta

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client(paciente):
    client = APIClient()
    client.force_authenticate(user=paciente)

    return client


@pytest.fixture
def especialidades():
    return [
        baker.make('core.Especialidade', nome='cardiologia'),
        baker.make('core.Especialidade', nome='pediatria')
    ]


@pytest.fixture
def medicos():
    return baker.make('core.Medico', _quantity=2)


def test_visualizar_especialidades(api_client, especialidades):
    res = api_client.get('/especialidades/')

    assert res.status_code == 200

    especialidades = sorted(especialidades, key=lambda e: e.nome)
    assert all(
        [a['id'] == b.id for a, b in zip(res.data, especialidades)]
    )


@pytest.mark.parametrize(
    'parametro,resultado', [
        ('card', 'cardiologia'),
        ('pediatria', 'pediatria')
    ]
)
def test_pesquisar_especialidade(api_client, especialidades, parametro, resultado):
   res = api_client.get(f'/especialidades/?search={parametro}')

   assert res.status_code == 200
   assert res.data[0]['nome'] == resultado


def test_visualizar_medicos(api_client, medicos):
    res = api_client.get('/medicos/')

    assert res.status_code == 200

    medicos = sorted(medicos, key=lambda m: m.nome)
    assert all(
        [a['id'] == b.id for a, b in zip(res.data, medicos)]
    )


def test_marcar_consulta(api_client, horario):
    payload = {
        'agenda_id': horario.agenda_id,
        'horario': horario.hora
    }

    res = api_client.post('/consultas/', payload)

    assert res.status_code == 201
    assert Consulta.objects.count() == 1


def test_desmarcar_consulta(api_client, consulta):
    res = api_client.delete(f'/consultas/{consulta.pk}/')

    assert res.status_code == 204
    assert Consulta.objects.count() == 0


def test_desmarcar_consulta_de_outro_paciente(api_client, consulta, paciente2):
    api_client.force_authenticate(user=paciente2)
    res = api_client.delete(f'/consultas/{consulta.pk}/')

    assert res.status_code == 404
    assert Consulta.objects.count() == 1


def test_visulizar_consultas(api_client, consulta, paciente2):
    consulta_outro_paciente = baker.make(Consulta, paciente=paciente2)

    res = api_client.get('/consultas/')
    consulta_ids = [c['id'] for c in res.data]

    assert res.status_code == 200

    assert len(res.data) == 1
    assert consulta.pk in consulta_ids

    assert consulta_outro_paciente.pk not in consulta_ids
