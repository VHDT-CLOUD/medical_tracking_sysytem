import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_tracking.settings')
django.setup()

from accounts.models import Hospital
from django.contrib.auth import get_user_model

def add_sample_hospital():
    # Create the hospital
    hospital = Hospital.objects.create(
        name="Sample Hospital",
        email="sample_hospital@example.com",
        address="123 Sample Street, Sample City",
        registration_number="REG123456",
        is_active=True
    )
    
    # Create a user for the hospital
    User = get_user_model()
    user = User.objects.create(
        username="hospital_sample",
        email="sample_hospital@example.com",
        is_hospital=True,
        registration_number="REG123456",
        hospital=hospital
    )
    user.set_password("sample123")
    user.save()
    
    print("Sample hospital and user added successfully.")
    print("Login with:")
    print("Registration Number: REG123456")
    print("Password: sample123")

if __name__ == "__main__":
    add_sample_hospital()
