from django import forms
from django.contrib.auth.forms import SetPasswordForm

class AadhaarVerificationForm(forms.Form):
    aadhaar_number = forms.CharField(max_length=12, required=True)

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)

class PasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=True)
