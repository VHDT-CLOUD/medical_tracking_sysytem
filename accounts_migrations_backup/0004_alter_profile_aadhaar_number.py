# Generated by Django 5.1.6 on 2025-04-09 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_fix_hospital_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='aadhaar_number',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('^\\d{12}$', 'Aadhaar number must be 12 digits')]),
        ),
    ]
