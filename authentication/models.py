from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
import random

# Custom user model extending AbstractUser
class CustomUser(AbstractUser):
    aadhaar_number = models.CharField(max_length=12, unique=True)  # Unique Aadhaar number
    phone = models.CharField(max_length=15, unique=True)  # Unique phone number
    email = models.EmailField(unique=True)  # Unique email address

    is_doctor = models.BooleanField(default=False)  # Flag to identify if the user is a doctor
    is_patient = models.BooleanField(default=False)  # Flag to identify if the user is a patient

    USERNAME_FIELD = 'aadhaar_number'
    REQUIRED_FIELDS = ['username', 'email', 'phone']

    def __str__(self):
        return self.username

# Hospital model to store hospital details
class Hospital(models.Model):
    name = models.CharField(max_length=255)  # Hospital name
    location = models.CharField(max_length=255)  # Hospital location
    phone = models.CharField(max_length=15)  # Hospital contact number

    def __str__(self):
        return self.name

# Patient model to store patient details
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Link to CustomUser
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # Link to Hospital
    name = models.CharField(max_length=255)  # Patient name
    phone = models.CharField(max_length=15, unique=True)  # Unique phone number
    email = models.EmailField(unique=True)  # Unique email address
    date_of_birth = models.DateField()  # Date of birth
    medical_history = models.TextField()  # Medical history

    def __str__(self):
        return self.name

# Doctor model to store doctor details
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Link to CustomUser
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # Link to Hospital
    name = models.CharField(max_length=255)  # Doctor name
    phone = models.CharField(max_length=15, unique=True)  # Unique phone number
    email = models.EmailField(unique=True)  # Unique email address
    specialization = models.CharField(max_length=100)  # Specialization field

    def __str__(self):
        return self.name

# MedicalRecord model to store medical records
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Link to Patient
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Link to Doctor
    # Additional fields for medical records can be added here
