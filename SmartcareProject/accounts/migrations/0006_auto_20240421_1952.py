# Generated by Django 3.0.5 on 2024-04-21 19:52

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20240421_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointmentDateTime',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointmentTime',
            field=models.TimeField(default=datetime.time(8, 0)),
            preserve_default=False,
        ),
    ]
