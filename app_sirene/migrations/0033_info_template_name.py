# Generated by Django 3.0 on 2019-12-28 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0032_auto_20191228_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='template_name',
            field=models.CharField(blank=True, max_length=120, verbose_name='Nom de modele'),
        ),
    ]
