from django.core.management.base import BaseCommand
from accounts.models import Hospital
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Set password for a hospital'

    def add_arguments(self, parser):
        parser.add_argument('--hospital_id', type=int, required=True, help='ID of the hospital')
        parser.add_argument('--password', type=str, required=True, help='New password for the hospital')

    def handle(self, *args, **options):
        try:
            # Check if hospital exists
            try:
                hospital = Hospital.objects.get(hospital_id=options['hospital_id'])
            except Hospital.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Hospital with ID {options['hospital_id']} does not exist"))
                return
            
            # Set the password
            hospital.set_password(options['password'])
            hospital.save()
            
            self.stdout.write(self.style.SUCCESS(f"Successfully set password for hospital: {hospital.name}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error setting hospital password: {str(e)}"))