import pytest

from model_bakery import baker

from ..serializers import (
    ConsultaSerializer,
    PACIENTE_COM_CONSULTA_MARCADA_MSG,
    HORARIO_INDISPONIVEL_MSG
)


@pytest.fixture
def req(rf, paciente):
    request = rf.post('/consultas')
    request.user = paciente

    return request


@pytest.fixture
def medico_dict(consulta):
    medico = consulta.medico
    especialidade = medico.especialidade

    return  {
        'id': medico.pk,
        'crm': medico.crm,
        'nome': medico.nome,
        'especialidade': {
            'id': especialidade.pk,
            'nome': especialidade.nome
        }
    }


@pytest.mark.django_db
class TestConsultaSerializer:
    def test_representacao(self, consulta, medico_dict):
        serializer = ConsultaSerializer(consulta)

        return serializer.data == {
            'id': consulta.pk,
            'dia': consulta.dia,
            'horario': consulta.horario,
            'data_agendamento': consulta.data_agendamento,
            'medico': medico_dict
        }

    def test_validar_paciente_com_consulta_marcada(self, consulta, horario, req):
        payload = {
            'horario': horario.hora,
            'agenda_id': horario.agenda_id
        }

        serializer = ConsultaSerializer(data=payload, context={'request': req})

        assert not serializer.is_valid()
        assert serializer.errors == {
            'non_field_errors': [PACIENTE_COM_CONSULTA_MARCADA_MSG]
        }

    def test_validar_horario_indisponivel(self, consulta, horario, paciente2, req):
        req.user = paciente2

        payload = {
            'horario': horario.hora,
            'agenda_id': horario.agenda_id
        }

        serializer = ConsultaSerializer(data=payload, context={'request': req})

        assert not serializer.is_valid()
        assert serializer.errors == {
            'horario': [HORARIO_INDISPONIVEL_MSG]
        }

    def test_payload_valido(self, req):
        horario = baker.make('core.AgendaHora')

        payload = {
            'horario': horario.hora,
            'agenda_id': horario.agenda_id
        }

        serializer = ConsultaSerializer(data=payload, context={'request': req})

        assert serializer.is_valid()
        assert serializer.errors == {}


