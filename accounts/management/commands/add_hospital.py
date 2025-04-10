from django.core.management.base import BaseCommand
from accounts.models import Hospital
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Add a new hospital to the system'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, required=True, help='Name of the hospital')
        parser.add_argument('--email', type=str, required=True, help='Email of the hospital')
        parser.add_argument('--contact_number', type=str, required=True, help='Contact number of the hospital')
        parser.add_argument('--address', type=str, required=True, help='Address of the hospital')
        parser.add_argument('--registration_number', type=str, required=True, help='Registration number of the hospital')

    def handle(self, *args, **options):
        try:
            # Check if hospital with this registration number already exists
            if Hospital.objects.filter(registration_number=options['registration_number']).exists():
                self.stdout.write(self.style.ERROR(f"Hospital with registration number {options['registration_number']} already exists"))
                return
            
            # Check if hospital with this email already exists
            if Hospital.objects.filter(email=options['email']).exists():
                self.stdout.write(self.style.ERROR(f"Hospital with email {options['email']} already exists"))
                return
            
            # Create the hospital
            hospital = Hospital.objects.create_hospital(
                name=options['name'],
                email=options['email'],
                contact_number=options['contact_number'],
                address=options['address'],
                registration_number=options['registration_number'],
                is_active=True
            )
            
            self.stdout.write(self.style.SUCCESS(f"Successfully added hospital: {options['name']} with ID: {hospital.hospital_id}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error adding hospital: {str(e)}"))