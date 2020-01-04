# Generated by Django 3.0 on 2019-12-23 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0018_auto_20191223_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='priority',
            field=models.IntegerField(choices=[(0, 'N/A'), (1, 'P1 Critique'), (2, 'P2 Elevé'), (3, 'P3 Moyen'), (4, 'P4 Faible')], default=0, verbose_name='Priorite'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='priority2',
            field=models.IntegerField(choices=[(0, 'N/A'), (1, 'P1 Critique'), (2, 'P2 Elevé'), (3, 'P3 Moyen'), (4, 'P4 Faible')], default=0, verbose_name='Priorite finale'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='status',
            field=models.IntegerField(choices=[(0, 'N/A'), (1, 'Suspecté'), (2, 'En cours'), (3, 'Terminé'), (4, 'Fermé (auto)')], default=0, verbose_name='Etat'),
        ),
    ]
