# Generated by Django 3.0.5 on 2020-04-22 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200421_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendahora',
            name='disponivel',
            field=models.BooleanField(default=True, editable=False, verbose_name='disponível'),
        ),
    ]
