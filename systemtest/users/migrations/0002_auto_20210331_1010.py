# Generated by Django 3.1.5 on 2021-03-31 10:10

from django.db import migrations, models
import systemtest.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mfs',
            field=systemtest.utils.models.CharFieldUpper(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='shift',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
