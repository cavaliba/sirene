# Generated by Django 2.1.7 on 2019-12-15 15:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0007_auto_20191215_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announce',
            name='show_on',
        ),
        migrations.AlterField(
            model_name='announce',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Publish'),
        ),
    ]