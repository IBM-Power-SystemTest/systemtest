# Generated by Django 3.1.5 on 2021-05-01 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesthistory',
            name='user',
            field=models.ForeignKey(help_text='User who made the last transaction', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='requestgroup',
            name='request_group_workspace',
            field=models.ForeignKey(default=1, help_text='Area where the system is', on_delete=django.db.models.deletion.PROTECT, to='pts.requestgroupworkspace', verbose_name='Area'),
        ),
        migrations.AddField(
            model_name='request',
            name='request_group',
            field=models.ForeignKey(help_text='Reqeust Group', on_delete=django.db.models.deletion.PROTECT, to='pts.requestgroup', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='request',
            name='request_status',
            field=models.ForeignKey(blank=True, default=1, help_text='Requirement status', on_delete=django.db.models.deletion.PROTECT, to='pts.requeststatus', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(help_text='User who made the last transaction', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
