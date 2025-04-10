import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.db import connection

# First, check what migrations are in the database
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM django_migrations WHERE app='accounts'")
    migrations = cursor.fetchall()
    print(f"Found {len(migrations)} migrations for accounts app in database:")
    for migration in migrations:
        print(migration)

# Create a backup directory for migrations
backup_dir = 'accounts_migrations_backup'
os.makedirs(backup_dir, exist_ok=True)

# Backup all existing migration files
migrations_dir = os.path.join('accounts', 'migrations')
for file in os.listdir(migrations_dir):
    if file.endswith('.py') and file != '__init__.py' and file != '_init_.py':
        src_path = os.path.join(migrations_dir, file)
        dst_path = os.path.join(backup_dir, file)
        if os.path.isfile(src_path):
            print(f"Backing up {file}")
            shutil.copy2(src_path, dst_path)

# Keep only the initial migration and __init__.py
for file in os.listdir(migrations_dir):
    if file.endswith('.py') and file != '__init__.py' and file != '_init_.py' and file != '0001_initial.py':
        file_path = os.path.join(migrations_dir, file)
        if os.path.isfile(file_path):
            print(f"Removing {file}")
            os.remove(file_path)

# Create a new migration to fix the hospital field
fix_migration_path = os.path.join(migrations_dir, '0002_fix_hospital_field.py')
with open(fix_migration_path, 'w') as f:
    f.write("""# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # First, remove the field if it exists to avoid any issues
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
""")
print("Created new fix migration")

# Reset the migrations in the database
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app='accounts' AND name != '0001_initial'")
    print("Reset migrations in database")

print("\nMigration reset completed. Now run:")
print("python manage.py migrate accounts 0001_initial")
print("python manage.py migrate accounts")