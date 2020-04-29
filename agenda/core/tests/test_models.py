from datetime import date, datetime
from unittest import mock

import pytest
from model_bakery import baker
from pytest_django.asserts import assertNumQueries, assertQuerysetEqual

from ..models import Agenda


@pytest.mark.django_db
class TestAgendaDisponivelManager:
    def test_nao_deve_retornar_agendas_sem_horarios_cadastrados(self):
        baker.make(Agenda, horarios=[])

        assert Agenda.disponiveis.count() == 0

    def test_nao_deve_retornar_agendas_de_datas_passadas(self):
        agenda1 = baker.make(Agenda, dia=date(2020, 11, 14))
        baker.make('core.AgendaHora', agenda=agenda1)

        agenda2 = baker.make(Agenda, dia=date(2020, 11, 16))
        baker.make('core.AgendaHora', agenda=agenda2)

        with mock.patch(
            'agenda.core.managers.timezone.now',
            return_value=datetime(2020, 11, 15)
        ):
            qs = Agenda.disponiveis.all()
            assertQuerysetEqual(qs, [agenda2.dia], lambda a: a.dia)

    def test_nao_deve_considerar_horarios_passados_como_disponiveis(self):
        agenda1 = baker.make(
            Agenda,
            dia=date(2020, 11, 15),
        )
        baker.make('core.AgendaHora', agenda=agenda1, hora='8:00')
        baker.make('core.AgendaHora', agenda=agenda1, hora='9:00')

        agenda2 = baker.make(
            Agenda,
            dia=date(2020, 11, 15),
        )
        baker.make('core.AgendaHora', agenda=agenda2, hora='10:30')
        baker.make('core.AgendaHora', agenda=agenda2, hora='11:00')

        with mock.patch(
            'agenda.core.managers.timezone.now',
            return_value=datetime(2020, 11, 15, 10)  # 15/11/2020 às 10h
        ):
            qs = Agenda.disponiveis.all()
            assertQuerysetEqual(qs, [agenda2.dia], lambda a: a.dia)

    def test_deve_retornar_apenas_agendas_com_horarios_disponiveis(self):
        """
        Deve retornar apenas agendas que possuam horários disponíveis,
        desconsiderando horários marcados e passados.
        """
        dia = date(2020, 11, 15)

        agenda1 = baker.make(Agenda, dia=dia)
        baker.make('core.AgendaHora', agenda=agenda1, hora='9:00')

        agenda2 = baker.make(Agenda, dia=dia)
        baker.make('core.AgendaHora', agenda=agenda2, hora='11:00', disponivel=False)

        agenda3 = baker.make(Agenda, dia=dia)
        baker.make('core.AgendaHora', agenda=agenda3, hora='9:00')
        baker.make('core.AgendaHora', agenda=agenda3, hora='11:00')
        baker.make('core.AgendaHora', agenda=agenda3, hora='11:30', disponivel=False)

        with mock.patch(
            'agenda.core.managers.timezone.now',
            return_value=datetime(2020, 11, 15, 10)  # 15/11/2020 às 10h
        ):
            qs = Agenda.disponiveis.all()
            assertQuerysetEqual(qs, [agenda3.pk], lambda a: a.pk)

    def test_carregar_apenas_horarios_disponiveis(self):
        """
        Deve fazer o prefetch apenas dos horários disponíveis a atribuir
        à um atributo chamado `horarios_disponiveis`
        """
        agenda = baker.make(Agenda, dia=date(2020, 11, 15))
        baker.make('core.AgendaHora', agenda=agenda, hora='9:00')
        baker.make('core.AgendaHora', agenda=agenda, hora='10:30')
        baker.make('core.AgendaHora', agenda=agenda, hora='11:30', disponivel=False)

        with mock.patch(
            'agenda.core.managers.timezone.now',
            return_value=datetime(2020, 11, 15, 10)  # 15/11/2020 às 10h
        ):
            agendas = Agenda.disponiveis.carregar_apenas_horarios_disponiveis()

            agenda = agendas[0]
            assert hasattr(agenda, 'horarios_disponiveis')
            assert all(
                [a.hora.strftime('%H:%M') == b for a, b in zip(agenda.horarios_disponiveis, ['10:30'])]
            )


@pytest.mark.django_db
def test_marcar_horario_como_indisponivel(consulta, horario):
    """
    Deve marcar o horário como indisponível quando a consulta for marcada
    """
    horario.refresh_from_db()
    assert not horario.disponivel


@pytest.mark.django_db
def test_marcar_horario_como_disponivel(consulta, horario):
    """
    Deve marcar o horário como disponível quando a consulta for desmarcada (deletada)
    """
    # Desmarca consulta
    consulta.delete()

    horario.refresh_from_db()
    assert horario.disponivel
