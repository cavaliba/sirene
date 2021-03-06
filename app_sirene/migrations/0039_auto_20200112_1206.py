# Generated by Django 3.0 on 2020-01-12 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0038_auto_20200104_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='notify_groups',
            field=models.ManyToManyField(blank=True, to='app_sirene.ContactGroup'),
        ),
        migrations.AlterField(
            model_name='info',
            name='services',
            field=models.ManyToManyField(blank=True, to='app_sirene.Service'),
        ),
        migrations.AlterField(
            model_name='info',
            name='sites',
            field=models.ManyToManyField(blank=True, to='app_sirene.Site'),
        ),
    ]
