# Generated by Django 3.0 on 2019-12-30 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sirene', '0034_auto_20191230_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Actif'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='want_email',
            field=models.BooleanField(default=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='want_sms',
            field=models.BooleanField(default=True, verbose_name='SMS'),
        ),
    ]
