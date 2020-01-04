# Generated by Django 2.1.7 on 2019-12-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('content', models.TextField(blank=True, max_length=2000, verbose_name='Content')),
                ('visible', models.BooleanField(default=True, verbose_name='Visible')),
                ('author', models.CharField(blank=True, max_length=200, verbose_name='Author')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('days', models.IntegerField(default=7, verbose_name='Days')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
