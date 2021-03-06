# Generated by Django 3.0.5 on 2020-04-21 20:39

import agenda.core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
                ('crm', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=11)),
                ('especialidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medicos', to='core.Especialidade')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField(validators=[agenda.core.models.validate_date])),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agendas', to='core.Medico')),
            ],
            options={
                'ordering': ['dia'],
                'unique_together': {('medico', 'dia')},
            },
        ),
        migrations.CreateModel(
            name='AgendaHora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.TimeField()),
                ('agenda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Agenda')),
            ],
            options={
                'verbose_name': 'Horário',
                'ordering': ['hora'],
                'unique_together': {('agenda', 'hora')},
            },
        ),
    ]
