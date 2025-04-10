import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from django.db import connection
from accounts.models import CustomUser, Hospital

print("=== Verifying database fix ===")

# Step 1: Check if required columns exist
print("\n=== Step 1: Checking database columns ===")
with connection.cursor() as cursor:
    # Check if hospital_id column exists
    cursor.execute("SHOW COLUMNS FROM accounts_customuser LIKE 'hospital_id'")
    result = cursor.fetchone()
    if result:
        print("✅ hospital_id column exists in accounts_customuser")
    else:
        print("❌ hospital_id column does not exist in accounts_customuser")
    
    # Check if is_doctor column exists
    cursor.execute("SHOW COLUMNS FROM accounts_customuser LIKE 'is_doctor'")
    result = cursor.fetchone()
    if result:
        print("✅ is_doctor column exists in accounts_customuser")
    else:
        print("❌ is_doctor column does not exist in accounts_customuser")

# Step 2: Check migrations
print("\n=== Step 2: Checking migrations ===")
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM django_migrations WHERE app='accounts'")
    migrations = cursor.fetchall()
    print(f"Found {len(migrations)} migrations for accounts app in database:")
    for migration in migrations:
        print(migration)

# Step 3: Check user-hospital relationships
print("\n=== Step 3: Checking user-hospital relationships ===")
hospital_users = CustomUser.objects.filter(is_hospital=True)
print(f"Found {hospital_users.count()} hospital users")

for user in hospital_users:
    if hasattr(user, 'hospital') and user.hospital:
        print(f"✅ User {user.username} has hospital: {user.hospital.name}")
    else:
        print(f"❌ User {user.username} has no hospital assigned")
        # Try to find a matching hospital
        if hasattr(user, 'registration_number') and user.registration_number:
            hospital = Hospital.objects.filter(registration_number=user.registration_number).first()
            if hospital:
                print(f"   Found matching hospital: {hospital.name}")
                print(f"   To fix, run: python manage.py shell")
                print(f"   Then execute:")
                print(f"   from accounts.models import CustomUser, Hospital")
                print(f"   user = CustomUser.objects.get(username='{user.username}')")
                print(f"   hospital = Hospital.objects.get(registration_number='{user.registration_number}')")
                print(f"   user.hospital = hospital")
                print(f"   user.save()")

print("\n=== Verification completed ===")
print("If all checks passed, your database should be fixed and working correctly.")