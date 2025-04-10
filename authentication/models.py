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

class AadhaarOTP(models.Model):
    aadhaar_number = models.CharField(max_length=12, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    def is_expired(self):
        return self.expires_at < now()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Aadhaar: {self.aadhaar_number}, OTP: {self.otp}"
