# Generated by Django 3.0.5 on 2020-04-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200421_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='crm',
            field=models.IntegerField(unique=True),
        ),
    ]