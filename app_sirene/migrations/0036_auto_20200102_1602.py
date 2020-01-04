# Generated by Django 3.0 on 2020-01-02 15:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0035_auto_20191230_1528'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InfoTemplate',
        ),
        migrations.AlterField(
            model_name='info',
            name='author',
            field=models.CharField(help_text="Saisir ici l'identité du déclarant de l'événement.", max_length=200, verbose_name='Auteur'),
        ),
        migrations.AlterField(
            model_name='info',
            name='downtime',
            field=models.IntegerField(blank=True, default=0, help_text='Indisponibilité estimée/définitive en minutes.', null=True, verbose_name='Indisponibilité'),
        ),
        migrations.AlterField(
            model_name='info',
            name='duration',
            field=models.IntegerField(blank=True, default=0, help_text='Durée estimée/définitive en minutes.', null=True, verbose_name='Durée'),
        ),
        migrations.AlterField(
            model_name='info',
            name='start',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='Format : dd/mm/YYYY hh:mm:ss', verbose_name='Début'),
        ),
    ]