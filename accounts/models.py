from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import os
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    aadhaar_number = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{12}$', 'Aadhaar number must be 12 digits')]
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?\d{10,15}$', 'Enter a valid phone number')]
    )
    email = models.EmailField(max_length=254, unique=True)
    hospital = models.ForeignKey(
        'Hospital',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_customuser_set',  # Ensure this is unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_customuser_permissions_set',  # Ensure this is unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    # User type flags
    is_patient = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    # Ensure superuser creation works correctly
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_hospital = True  # Automatically set is_hospital for superusers
        super().save(*args, **kwargs)

    # For hospital users, store the registration number
    registration_number = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_dashboard_url(self):
        """
        Returns the dashboard URL based on the user type.
        """
        if self.is_patient:
            return '/patient/dashboard/'
        elif self.is_hospital:
            return '/hospital/dashboard/'
        else:
            return '/'

    def clean(self):
        """
        Ensure aadhaar_number contains exactly 12 digits and no extra spaces.
        """
        if self.aadhaar_number:
            self.aadhaar_number = self.aadhaar_number.strip()
            if not self.aadhaar_number.isdigit() or len(self.aadhaar_number) != 12:
                raise ValueError("Aadhaar number must be exactly 12 digits.")
        super().clean()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    aadhaar_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[RegexValidator(r'^\d{12}$', 'Aadhaar number must be 12 digits')]
    )
    # Other fields...

    def __str__(self):
        return self.user.username

    def clean(self):
        """
        Ensure aadhaar_number contains exactly 12 digits and no extra spaces.
        """
        if self.aadhaar_number:
            self.aadhaar_number = self.aadhaar_number.strip()
            if not self.aadhaar_number.isdigit() or len(self.aadhaar_number) != 12:
                raise ValueError("Aadhaar number must be exactly 12 digits.")
        super().clean()

class HospitalManager(models.Manager):
    def create_hospital(self, name, email, address, registration_number, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')

        # Create a CustomUser for this hospital
        from django.contrib.auth.hashers import make_password
        password = extra_fields.pop('password', None)

        # Create the hospital record
        hospital = self.model(
            name=name,
            email=email,
            address=address,
            registration_number=registration_number,
            **extra_fields
        )
        hospital.save(using=self._db)

        # Create the user account for this hospital
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Username will be "hospital_" + registration_number
        username = f"hospital_{registration_number}"

        # Check if a user with this username already exists
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            # Update the existing user
            existing_user.email = email
            existing_user.is_hospital = True
            existing_user.registration_number = registration_number
            existing_user.hospital = hospital
            
            if password:
                existing_user.set_password(password)
            
            existing_user.save()
            user = existing_user
        else:
            # Create a new user
            user = User.objects.create(
                username=username,
                email=email,
                is_hospital=True,
                registration_number=registration_number,
                hospital=hospital
            )

            if password:
                user.set_password(password)
            else:
                # Set an unusable password if none provided
                user.set_unusable_password()

            user.save()

        return hospital

class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    address = models.TextField()

    objects = HospitalManager()

    def __str__(self):
        return self.name

    def get_user(self):
        """
        Get the CustomUser associated with this hospital
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        # First try to find by hospital relationship
        user = User.objects.filter(hospital=self).first()
        if user:
            return user
        # If not found, try by registration number
        return User.objects.filter(is_hospital=True, registration_number=self.registration_number).first()

    def set_password(self, raw_password):
        """
        Sets the password for the hospital's user account
        """
        user = self.get_user()
        if user:
            user.set_password(raw_password)
            user.save()

    def check_password(self, raw_password):
        """
        Checks if the provided password matches the hospital user's password
        """
        user = self.get_user()
        if user:
            return user.check_password(raw_password)
        return False

    def can_access_patient(self, patient):
        return patient.hospital == self

    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'
        ordering = ['name']

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

field_name = models.CharField(max_length=255, default='default_value')

def document_upload_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/medical_records/patient_<id>/<filename>
    return f'medical_records/patient_{instance.medical_record.patient.id}/{filename}'

class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)  # Ensure 'Doctor' is quoted
    diagnosis = models.TextField()
    prescription = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # Fix missing parenthesis
    record_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)  # Allow notes to be optional
    document = models.FileField(upload_to='medical_records/', blank=True, null=True)  # Allow document to be optional

    def save(self, *args, **kwargs):
        # Ensure record_date is not in the future
        if self.record_date > timezone.now():
            raise ValueError("Record date cannot be in the future.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Record {self.record_id} for {self.patient.full_name}"

class MedicalDocument(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to=document_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.document.name)

    def __str__(self):
        return f"Document for {self.medical_record}"

class AadhaarOTP(models.Model):
    aadhaar_number = models.CharField(max_length=12)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.aadhaar_number}"

    class Meta:
        verbose_name = 'Aadhaar OTP'
        verbose_name_plural = 'Aadhaar OTPs'

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return f"Dr. {self.full_name} ({self.specialization})"
