# Generated by Django 3.0.5 on 2024-04-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_patient_assigneddoctorid'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
