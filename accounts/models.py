from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random
from datetime import timedelta
from django.utils.timezone import now

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, aadhaar, password=None, **extra_fields):
        if not aadhaar:
            raise ValueError("The Aadhaar number is required")
        user = self.model(aadhaar=aadhaar, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, aadhaar, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(aadhaar, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    aadhaar = models.CharField(max_length=12, unique=True, verbose_name="Aadhaar Number")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "aadhaar"
    REQUIRED_FIELDS = []

    def _str_(self):
        return self.aadhaar

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

# Hospital Model
class Hospital(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15, unique=True)

    def _str_(self):
        return self.name

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"

# Patient Model
class Patient(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    aadhaar_number = models.CharField(max_length=12, unique=True, verbose_name="Aadhaar Number")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="patient_profile", null=True, blank=True)

    def _str_(self):
        return self.name

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

# Doctor Model
class Doctor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="doctors")

    def _str_(self):
        return f"{self.name} ({self.specialization})"

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

# Medical Record Model
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="records")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="patients")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="records")
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Record for {self.patient.name} by {self.doctor.name} at {self.hospital.name}"

    class Meta:
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"

# Aadhaar OTP Model
class AadhaarOTP(models.Model):
    aadhaar_number = models.CharField(max_length=12, verbose_name="Aadhaar Number")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        unique_together = ['aadhaar_number', 'otp']  # Ensure OTP is unique for each Aadhaar number

    @staticmethod
    def generate_otp():
        """Generates a Unique 6-digit OTP"""
        return f"{random.randint(100000, 999999)}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=5)  # OTP valid for 5 minutes
        super().save(*args, **kwargs)

    def is_valid(self):
        return now() <= self.expires_at

    def _str_(self):
        return f"OTP for {self.aadhaar_number} (Valid till: {self.expires_at})"

    class Meta:
        verbose_name = "Aadhaar OTP"
        verbose_name_plural = "Aadhaar OTPs"