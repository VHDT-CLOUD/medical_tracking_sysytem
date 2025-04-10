from django.contrib import admin
from .models import CustomUser, Hospital, Patient, MedicalRecord, AadhaarOTP

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'username', 'email', 'phone', 'is_patient', 'hospital')  # Removed 'is_doctor'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'aadhaar_number', 'phone_number', 'dob')

class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address', 'registration_number')  # Removed 'contact_number'

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'hospital', 'diagnosis', 'record_date')  # Ensure 'doctor' is valid
    search_fields = ('patient__full_name', 'doctor__full_name', 'hospital__name', 'diagnosis', 'prescription')

class AadhaarOTPAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'otp', 'created_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(AadhaarOTP, AadhaarOTPAdmin)