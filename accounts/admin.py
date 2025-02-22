from django.contrib import admin
from .models import CustomUser, Hospital, Patient, Doctor, MedicalRecord, AadhaarOTP

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'username', 'email', 'phone', 'is_doctor', 'is_patient')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_aadhaar', 'email', 'phone', 'hospital')

    def get_aadhaar(self, obj):
        return obj.user.aadhaar_number
    get_aadhaar.short_description = 'Aadhaar Number'

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'hospital', 'specialization')

class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone')

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'hospital', 'diagnosis', 'created_at')

class AadhaarOTPAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'otp', 'created_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(AadhaarOTP, AadhaarOTPAdmin)