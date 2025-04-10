from django.core.management.base import BaseCommand
from accounts.models import Hospital, Doctor, CustomUser
from django.db import transaction
from django.contrib.auth.hashers import make_password
import random
import string

class Command(BaseCommand):
    help = 'Creates sample hospitals and doctors for testing'

    def generate_random_aadhaar(self):
        """Generate a random 12-digit Aadhaar number"""
        return ''.join(random.choices(string.digits, k=12))

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Create sample hospitals
        hospitals = [
            {
                'name': 'City General Hospital',
                'location': 'Downtown, City',
                'phone': '1234567890'
            },
            {
                'name': 'Community Health Center',
                'location': 'Suburb Area, City',
                'phone': '2345678901'
            },
            {
                'name': 'Medical Specialists Clinic',
                'location': 'Uptown, City',
                'phone': '3456789012'
            }
        ]

        # Create sample doctors
        doctors = [
            {
                'name': 'Dr. John Smith',
                'specialization': 'Cardiology',
                'phone': '4567890123',
                'email': 'john.smith@example.com',
                'hospital_name': 'City General Hospital'
            },
            {
                'name': 'Dr. Sarah Johnson',
                'specialization': 'Pediatrics',
                'phone': '5678901234',
                'email': 'sarah.johnson@example.com',
                'hospital_name': 'Community Health Center'
            },
            {
                'name': 'Dr. Michael Brown',
                'specialization': 'Orthopedics',
                'phone': '6789012345',
                'email': 'michael.brown@example.com',
                'hospital_name': 'Medical Specialists Clinic'
            },
            {
                'name': 'Dr. Emily Davis',
                'specialization': 'Neurology',
                'phone': '7890123456',
                'email': 'emily.davis@example.com',
                'hospital_name': 'City General Hospital'
            },
            {
                'name': 'Dr. Robert Wilson',
                'specialization': 'Dermatology',
                'phone': '8901234567',
                'email': 'robert.wilson@example.com',
                'hospital_name': 'Community Health Center'
            }
        ]

        # Create hospitals
        created_hospitals = {}
        for hospital_data in hospitals:
            hospital, created = Hospital.objects.get_or_create(
                name=hospital_data['name'],
                defaults={
                    'location': hospital_data['location'],
                    'phone': hospital_data['phone']
                }
            )
            created_hospitals[hospital.name] = hospital
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created hospital: {hospital.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Hospital already exists: {hospital.name}'))

        # Create doctors
        for doctor_data in doctors:
            hospital = created_hospitals.get(doctor_data['hospital_name'])
            if not hospital:
                self.stdout.write(self.style.ERROR(f"Hospital not found: {doctor_data['hospital_name']}"))
                continue

            # Check if doctor with this email already exists
            if Doctor.objects.filter(email=doctor_data['email']).exists():
                self.stdout.write(self.style.WARNING(f"Doctor already exists with email: {doctor_data['email']}"))
                continue

            # Create a user for the doctor
            aadhaar_number = self.generate_random_aadhaar()
            username = doctor_data['email'].split('@')[0]

            # Make sure the aadhaar number is unique
            while CustomUser.objects.filter(aadhaar_number=aadhaar_number).exists():
                aadhaar_number = self.generate_random_aadhaar()

            # Create the user
            user = CustomUser.objects.create(
                username=username,
                aadhaar_number=aadhaar_number,
                email=doctor_data['email'],
                phone=doctor_data['phone'],
                first_name=doctor_data['name'].replace('Dr. ', ''),
                password=make_password('Password@123'),  # Default password
                is_doctor=True
            )

            # Create the doctor
            doctor = Doctor.objects.create(
                user=user,
                name=doctor_data['name'],
                specialization=doctor_data['specialization'],
                phone=doctor_data['phone'],
                email=doctor_data['email'],
                hospital=hospital
            )

            self.stdout.write(self.style.SUCCESS(f'Created doctor: {doctor.name} with user: {user.username}'))

        self.stdout.write(self.style.SUCCESS('Sample data creation completed!'))