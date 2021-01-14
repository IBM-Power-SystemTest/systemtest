# Generated by Django 3.1.5 on 2021-01-14 04:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ncm_tag', models.PositiveIntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MaxValueValidator(99999999)])),
            ],
            options={
                'db_table': 'pts_request',
            },
        ),
        migrations.CreateModel(
            name='RequestGroupStatus',
            fields=[
                ('id', models.SmallAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'pts_request_group_status',
            },
        ),
        migrations.CreateModel(
            name='RequestGroupWorkspace',
            fields=[
                ('id', models.SmallAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'pts_request_group_workspace',
            },
        ),
        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('id', models.SmallAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'pts_request_status',
            },
        ),
        migrations.CreateModel(
            name='RequestTrackStatus',
            fields=[
                ('id', models.SmallAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'pts_request_track_status',
            },
        ),
        migrations.CreateModel(
            name='RequestTrack',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('part_number', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]{7}$')])),
                ('serial_number', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]{12}$')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pts.request')),
                ('request_track_status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='pts.requesttrackstatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pts_request_track',
            },
        ),
        migrations.CreateModel(
            name='RequestGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_description', models.CharField(max_length=15)),
                ('part_number', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]{7}$')])),
                ('is_vpd', models.BooleanField(default=False)),
                ('is_serialized', models.BooleanField(default=True)),
                ('system_number', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]{7}$')])),
                ('system_cell', models.CharField(max_length=4, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-z0-9]{4}$')])),
                ('is_loaner', models.BooleanField(default=False)),
                ('qty', models.SmallIntegerField(default=1)),
                ('request_bay', models.CharField(max_length=4, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-z0-9]{4}$')])),
                ('request_group_status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='pts.requestgroupstatus')),
                ('request_group_workspace', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='pts.requestgroupworkspace')),
            ],
            options={
                'db_table': 'pts_request_group',
            },
        ),
        migrations.AddField(
            model_name='request',
            name='request_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pts.requestgroup'),
        ),
        migrations.AddField(
            model_name='request',
            name='request_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='pts.requeststatus'),
        ),
    ]