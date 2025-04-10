import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.db import connection

# Check if django_migrations table exists
with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES LIKE 'django_migrations'")
    if cursor.fetchone():
        print("django_migrations table exists")
        cursor.execute("SELECT * FROM django_migrations WHERE app='accounts'")
        migrations = cursor.fetchall()
        print(f"Found {len(migrations)} migrations for accounts app:")
        for migration in migrations:
            print(migration)
    else:
        print("django_migrations table does not exist")

# Check if hospital_id column exists in accounts_customuser
with connection.cursor() as cursor:
    cursor.execute("SHOW COLUMNS FROM accounts_customuser LIKE 'hospital_id'")
    result = cursor.fetchone()
    if result:
        print("hospital_id column exists in accounts_customuser")
    else:
        print("hospital_id column does not exist in accounts_customuser")

# Check if is_doctor column exists in accounts_customuser
with connection.cursor() as cursor:
    cursor.execute("SHOW COLUMNS FROM accounts_customuser LIKE 'is_doctor'")
    result = cursor.fetchone()
    if result:
        print("is_doctor column exists in accounts_customuser")
    else:
        print("is_doctor column does not exist in accounts_customuser")