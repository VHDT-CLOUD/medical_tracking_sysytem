from django.contrib import admin
from .models import CustomUser, Patient, Doctor, Hospital, MedicalRecord, AadhaarOTP

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(MedicalRecord)
admin.site.register(AadhaarOTP)
