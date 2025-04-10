# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_add_is_doctor_field'),
    ]

    operations = [
        # First, remove the field if it exists
        migrations.RemoveField(
            model_name='customuser',
            name='hospital',
        ),
        # Then add it back with the correct definition
        migrations.AddField(
            model_name='customuser',
            name='hospital',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='users',
                to='accounts.hospital'
            ),
        ),
    ]