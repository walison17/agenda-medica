# Generated by Django 3.0.5 on 2020-04-21 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='medico',
            name='telefone',
            field=models.CharField(blank=True, max_length=11),
        ),
    ]
