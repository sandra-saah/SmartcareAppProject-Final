# Generated by Django 3.0.5 on 2024-04-21 19:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20240421_1939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointmentDate',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointmentDateTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]