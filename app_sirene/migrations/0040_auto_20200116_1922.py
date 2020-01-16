# Generated by Django 3.0 on 2020-01-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0039_auto_20200112_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='site',
        ),
        migrations.AddField(
            model_name='contact',
            name='comment',
            field=models.CharField(blank=True, max_length=128, verbose_name='Commentaire'),
        ),
    ]
