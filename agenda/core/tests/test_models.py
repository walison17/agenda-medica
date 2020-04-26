from datetime import date, datetime
from unittest import mock

import pytest
from model_bakery import baker
from pytest_django.asserts import assertNumQueries

from ..models import Agenda


@pytest.mark.django_db
class TestAgendaDisponivelManager:
    def test_nao_deve_retornar_agendas_de_datas_passadas(self):
        baker.make(Agenda, dia=date(2020, 11, 14), horarios__disponivel=True, _quantity=4)
        baker.make(Agenda, dia=date(2020, 11, 16), horarios__disponivel=True, _quantity=2)

        with mock.patch('agenda.core.managers.timezone.now', return_value=datetime(2020, 11, 15)):
            assert Agenda.disponiveis.count() == 2
            assert Agenda.objects.count() == 6

    def test_nao_deve_retornar_horarios_passados(self):
        baker.make(
            Agenda,
            dia=date(2020, 11, 15),
            horarios__disponivel=True,
            horarios__hora='09:00'
        )
        baker.make(
            Agenda,
            dia=date(2020, 11, 15),
            horarios__disponivel=True,
            horarios__hora='11:00'
        )

        with mock.patch('agenda.core.managers.timezone.now', return_value=datetime(2020, 11, 15, hour=10, minute=0)):
            assert Agenda.disponiveis.count() == 1
            assert Agenda.objects.count() == 2

    def test_deve_retornar_apenas_agendas_que_possuam_pelo_menos_um_horario_disponivel(self):
        baker.make(Agenda, dia=date(2020, 11, 16), horarios__disponivel=False, _quantity=2)
        baker.make(Agenda, dia=date(2020, 11, 17), horarios__disponivel=True, _quantity=1)
        baker.make(Agenda, dia=date(2020, 11, 18), horarios__disponivel=False, _quantity=1)

        with mock.patch('agenda.core.managers.timezone.now', return_value=datetime(2020, 11, 15)):
            assert Agenda.disponiveis.count() == 1
            assert Agenda.objects.count() == 4

    def test_carregar_apenas_horarios_disponiveis(self):
        agenda = baker.make(Agenda, dia=date(2020, 11, 17))

        baker.make('core.AgendaHora', agenda=agenda, hora='08:00')
        baker.make('core.AgendaHora', agenda=agenda, hora='08:30')
        baker.make('core.AgendaHora', agenda=agenda, hora='09:00', disponivel=False)

        with assertNumQueries(2):
            agenda = Agenda.disponiveis.carregar_apenas_horarios_disponiveis()

            assert len(agenda[0].horarios_disponiveis) == 2
