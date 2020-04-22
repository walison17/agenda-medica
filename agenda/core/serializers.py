from datetime import date

from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import Especialidade, Medico, Agenda, Consulta


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ['id', 'nome']


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer()

    class Meta:
        model = Medico
        fields = [
            'id',
            'crm',
            'nome',
            'especialidade',
        ]


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer()
    horarios = serializers.StringRelatedField(many=True, source='horarios_disponiveis')

    class Meta:
        model = Agenda
        fields = [
            'id',
            'medico',
            'dia',
            'horarios'
        ]


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user


class ConsultaSerializer(serializers.ModelSerializer):
    agenda_id = serializers.PrimaryKeyRelatedField(
        queryset=Agenda.objects.filter(dia__gte=date.today()),
        write_only=True,
        label='agenda'
    )
    medico = MedicoSerializer(read_only=True)
    paciente = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Consulta
        fields = [
            'id',
            'dia',
            'horario',
            'data_agendamento',
            'medico',
            'paciente',
            'agenda_id'
        ]
        read_only_fields = [
            'dia',
            'data_agendamento'
        ]

    def validate(self, data):
        agenda = data['agenda_id']
        horario = data['horario']

        if (
            Consulta
            .objects
            .filter(
                dia=agenda.dia,
                horario=horario,
                paciente=data['paciente'],
            )
            .exists()
        ):
            raise ValidationError(
                'Paciente já possui uma consulta marcada para esse dia e horário'
            )

        return data

    def create(self, data):
        agenda = data.pop('agenda_id')

        return Consulta.objects.create(
            dia=agenda.dia,
            medico=agenda.medico,
            **data
        )
