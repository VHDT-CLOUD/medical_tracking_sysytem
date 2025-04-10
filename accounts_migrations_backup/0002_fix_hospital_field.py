# Generated manually

from django.db import migrations, models
from django.db.utils import OperationalError
import django.db.models.deletion

def ensure_hospital_table(apps, schema_editor):
    """Ensure the accounts_hospital table and hospital_id column exist."""
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        try:
            # Check if the table exists
            cursor.execute("""
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = 'accounts_hospital';
            """)
            if cursor.fetchone()[0] == 0:
                # Create the table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE accounts_hospital (
                        hospital_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(254) UNIQUE NOT NULL,
                        address TEXT NOT NULL,
                        registration_number VARCHAR(50) UNIQUE NOT NULL,
                        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE
                    );
                """)
            else:
                # Ensure the hospital_id column exists and is the primary key
                cursor.execute("""
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = 'accounts_hospital' AND COLUMN_NAME = 'hospital_id';
                """)
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE accounts_hospital ADD COLUMN hospital_id INT AUTO_INCREMENT PRIMARY KEY;")
        except OperationalError as e:
            raise RuntimeError(f"Failed to ensure accounts_hospital table: {e}")

def safe_remove_hospital_id(apps, schema_editor):
    """Safely remove the hospital_id column if it exists."""
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'accounts_customuser' AND COLUMN_NAME = 'hospital_id';
            """)
            if cursor.fetchone():
                cursor.execute("ALTER TABLE accounts_customuser DROP COLUMN hospital_id;")
        except OperationalError:
            pass  # Ignore if the column does not exist

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(ensure_hospital_table),
        migrations.RunPython(safe_remove_hospital_id),
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