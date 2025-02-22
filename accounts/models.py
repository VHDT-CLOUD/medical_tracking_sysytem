from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
import random
class CustomUser(AbstractUser):
    aadhaar_number = models.CharField(max_length=12, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    USERNAME_FIELD = 'aadhaar_number'
    REQUIRED_FIELDS = ['username', 'email', 'phone']

    def __str__(self):
        return self.username

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    medical_history = models.TextField()

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.patient.name} by {self.doctor.name}"

class AadhaarOTP(models.Model):
    aadhaar_number = models.CharField(max_length=12)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.aadhaar_number}"

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
