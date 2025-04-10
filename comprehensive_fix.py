import os
import django
import shutil
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.db import connection

print("=== Starting comprehensive database fix ===")

# Step 1: Backup all migration files
print("\n=== Step 1: Backing up migration files ===")
backup_dir = 'accounts_migrations_backup'
os.makedirs(backup_dir, exist_ok=True)

migrations_dir = os.path.join('accounts', 'migrations')
for file in os.listdir(migrations_dir):
    if file.endswith('.py') and file != '__init__.py' and file != '_init_.py':
        src_path = os.path.join(migrations_dir, file)
        dst_path = os.path.join(backup_dir, file)
        if os.path.isfile(src_path):
            print(f"Backing up {file}")
            shutil.copy2(src_path, dst_path)

# Step 2: Check database state
print("\n=== Step 2: Checking database state ===")
with connection.cursor() as cursor:
    # Check migrations
    cursor.execute("SELECT * FROM django_migrations WHERE app='accounts'")
    migrations = cursor.fetchall()
    print(f"Found {len(migrations)} migrations for accounts app in database:")
    for migration in migrations:
        print(migration)
    
    # Check if hospital_id column exists
    cursor.execute("SHOW COLUMNS FROM accounts_customuser LIKE 'hospital_id'")
    result = cursor.fetchone()
    if result:
        print("hospital_id column exists in accounts_customuser")
    else:
        print("hospital_id column does not exist in accounts_customuser")
    
    # Check if is_doctor column exists
    cursor.execute("SHOW COLUMNS FROM accounts_customuser LIKE 'is_doctor'")
    result = cursor.fetchone()
    if result:
        print("is_doctor column exists in accounts_customuser")
    else:
        print("is_doctor column does not exist in accounts_customuser")

# Step 3: Fix the database directly if needed
print("\n=== Step 3: Fixing database directly if needed ===")
with connection.cursor() as cursor:
    # Check if hospital_id column exists
    cursor.execute("SHOW COLUMNS FROM accounts_customuser LIKE 'hospital_id'")
    hospital_id_exists = cursor.fetchone() is not None
    
    # Add hospital_id column if it doesn't exist
    if not hospital_id_exists:
        print("Adding hospital_id column to accounts_customuser table...")
        try:
            cursor.execute("""
            ALTER TABLE accounts_customuser 
            ADD COLUMN hospital_id INT NULL,
            ADD CONSTRAINT fk_hospital 
            FOREIGN KEY (hospital_id) 
            REFERENCES accounts_hospital(hospital_id) 
            ON DELETE SET NULL;
            """)
            print("Successfully added hospital_id column")
        except Exception as e:
            print(f"Error adding hospital_id column: {e}")
    else:
        print("hospital_id column already exists, no need to add it")
    
    # Check if is_doctor column exists
    cursor.execute("SHOW COLUMNS FROM accounts_customuser LIKE 'is_doctor'")
    is_doctor_exists = cursor.fetchone() is not None
    
    # Add is_doctor column if it doesn't exist
    if not is_doctor_exists:
        print("Adding is_doctor column to accounts_customuser table...")
        try:
            cursor.execute("""
            ALTER TABLE accounts_customuser 
            ADD COLUMN is_doctor BOOLEAN DEFAULT FALSE;
            """)
            print("Successfully added is_doctor column")
        except Exception as e:
            print(f"Error adding is_doctor column: {e}")
    else:
        print("is_doctor column already exists, no need to add it")

# Step 4: Reset migrations in the database
print("\n=== Step 4: Resetting migrations in the database ===")
with connection.cursor() as cursor:
    try:
        cursor.execute("DELETE FROM django_migrations WHERE app='accounts' AND name != '0001_initial'")
        print("Successfully reset migrations in database")
    except Exception as e:
        print(f"Error resetting migrations: {e}")

# Step 5: Clean up migration files
print("\n=== Step 5: Cleaning up migration files ===")
for file in os.listdir(migrations_dir):
    if file.endswith('.py') and file != '__init__.py' and file != '_init_.py' and file != '0001_initial.py':
        file_path = os.path.join(migrations_dir, file)
        if os.path.isfile(file_path):
            print(f"Removing {file}")
            os.remove(file_path)

# Step 6: Create a new migration to fix the hospital field
print("\n=== Step 6: Creating new fix migration ===")
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
        # Add is_doctor field if it doesn't exist
        migrations.AddField(
            model_name='customuser',
            name='is_doctor',
            field=models.BooleanField(default=False),
        ),
    ]
""")
print("Created new fix migration")

# Step 7: Apply migrations
print("\n=== Step 7: Applying migrations ===")
try:
    # Apply only the initial migration first
    result = subprocess.run(
        ['python', 'manage.py', 'migrate', 'accounts', '0001_initial', '--fake'],
        capture_output=True,
        text=True
    )
    print("Applied initial migration:")
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    # Then apply our fix migration
    result = subprocess.run(
        ['python', 'manage.py', 'migrate', 'accounts', '0002_fix_hospital_field'],
        capture_output=True,
        text=True
    )
    print("Applied fix migration:")
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    # Finally, make and apply any remaining migrations
    result = subprocess.run(
        ['python', 'manage.py', 'makemigrations', 'accounts'],
        capture_output=True,
        text=True
    )
    print("Made new migrations:")
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    result = subprocess.run(
        ['python', 'manage.py', 'migrate'],
        capture_output=True,
        text=True
    )
    print("Applied all migrations:")
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
except Exception as e:
    print(f"Error applying migrations: {e}")

print("\n=== Comprehensive fix completed ===")
print("Please test your application now to ensure everything is working correctly.")