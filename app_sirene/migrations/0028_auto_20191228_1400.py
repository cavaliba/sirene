# Generated by Django 3.0 on 2019-12-28 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0027_auto_20191228_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='hide',
            field=models.BooleanField(default=False, verbose_name='Masquer'),
        ),
        migrations.AlterField(
            model_name='info',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Création'),
        ),
        migrations.AlterField(
            model_name='info',
            name='updated_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Mise à jour'),
        ),
    ]
