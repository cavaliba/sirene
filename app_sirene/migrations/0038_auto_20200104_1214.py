# Generated by Django 3.0 on 2020-01-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0037_auto_20200102_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='detail',
            field=models.TextField(blank=True, max_length=4000, null=True, verbose_name='Description'),
        ),
    ]