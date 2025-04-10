from django.core.management.base import BaseCommand
from accounts.models import Doctor, Hospital
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Add a new doctor to the system'

    def add_arguments(self, parser):
        parser.add_argument('--full_name', type=str, required=True, help='Full name of the doctor')
        parser.add_argument('--email', type=str, required=True, help='Email of the doctor')
        parser.add_argument('--password', type=str, required=True, help='Password for the doctor')
        parser.add_argument('--hospital_id', type=int, required=True, help='Hospital ID the doctor belongs to')
        parser.add_argument('--specialization', type=str, required=True, help='Specialization of the doctor')
        parser.add_argument('--license_number', type=str, required=True, help='License number of the doctor')
        parser.add_argument('--phone_number', type=str, required=True, help='Phone number of the doctor')

    def handle(self, *args, **options):
        try:
            # Check if hospital exists
            try:
                hospital = Hospital.objects.get(hospital_id=options['hospital_id'])
            except Hospital.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Hospital with ID {options['hospital_id']} does not exist"))
                return
            
            # Check if doctor with this license number already exists
            if Doctor.objects.filter(license_number=options['license_number']).exists():
                self.stdout.write(self.style.ERROR(f"Doctor with license number {options['license_number']} already exists"))
                return
            
            # Check if doctor with this email already exists
            if Doctor.objects.filter(email=options['email']).exists():
                self.stdout.write(self.style.ERROR(f"Doctor with email {options['email']} already exists"))
                return
            
            # Create the doctor
            doctor = Doctor(
                full_name=options['full_name'],
                email=options['email'],
                password=make_password(options['password']),  # Hash the password
                hospital=hospital,
                specialization=options['specialization'],
                license_number=options['license_number'],
                phone_number=options['phone_number']
            )
            doctor.save()
            
            self.stdout.write(self.style.SUCCESS(f"Successfully added doctor: {options['full_name']}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error adding doctor: {str(e)}"))