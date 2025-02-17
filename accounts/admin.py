from django.contrib import admin
from .models import CustomUser, Hospital, Patient, Doctor, MedicalRecord, AadhaarOTP

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("aadhaar", "is_staff", "is_active", "date_joined")
    search_fields = ("aadhaar",)

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name",)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "aadhaar_number", "email", "phone")
    search_fields = ("name", "aadhaar_number")

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "hospital")
    search_fields = ("name", "specialization")

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "hospital", "created_at")
    search_fields = ("patient_name", "doctor_name")

@admin.register(AadhaarOTP)
class AadhaarOTPAdmin(admin.ModelAdmin):
    list_display = ("aadhaar_number", "otp", "expires_at")