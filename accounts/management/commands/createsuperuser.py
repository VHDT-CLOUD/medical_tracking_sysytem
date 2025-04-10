from django.core.management.base import BaseCommand
from accounts.models import CustomUser, Hospital
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Create a superuser for hospital login"

    def handle(self, *args, **kwargs):
        username = input("Enter username: ").strip()
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()
        hospital_name = input("Enter hospital name: ").strip()
        registration_number = input("Enter hospital registration number: ").strip()

        # Create the hospital record
        hospital, created = Hospital.objects.get_or_create(
            name=hospital_name,
            email=email,
            registration_number=registration_number,
            defaults={"address": "Default Address"}
        )

        # Create the superuser
        user = CustomUser.objects.create(
            username=username,
            email=email,
            is_superuser=True,
            is_staff=True,
            is_hospital=True,
            hospital=hospital,
            registration_number=registration_number
        )
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Superuser for hospital '{hospital_name}' created successfully!"))
