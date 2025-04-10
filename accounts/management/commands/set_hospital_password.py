from django.core.management.base import BaseCommand
from accounts.models import Hospital
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Set or update the password for a hospital"

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help="The email of the hospital")
        parser.add_argument('password', type=str, help="The new password for the hospital")

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        password = kwargs['password']

        try:
            hospital = Hospital.objects.get(email=email)
            hospital_user = hospital.get_user()  # Get the associated CustomUser
            if hospital_user:
                hospital_user.set_password(password)
                hospital_user.save()
                self.stdout.write(self.style.SUCCESS(f"Password updated successfully for hospital with email: {email}"))
            else:
                self.stdout.write(self.style.ERROR(f"No associated user found for hospital with email: {email}"))
        except Hospital.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Hospital with email {email} does not exist."))