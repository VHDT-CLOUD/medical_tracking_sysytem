import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

def generate_otp(length=6):
    """Generate a numeric OTP of specified length"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp):
    """Send OTP via email"""
    subject = 'Email Verification OTP - Medical Tracking System'
    message = f'''
    Thank you for registering with Medical Tracking System.
    
    Your OTP for email verification is: {otp}
    
    This OTP will expire in 10 minutes.
    
    If you did not request this OTP, please ignore this email.
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def store_otp(email, otp):
    """Store OTP in cache with 10-minute expiry"""
    cache_key = f"email_otp_{email}"
    cache.set(cache_key, otp, timeout=600)  # 600 seconds = 10 minutes

def verify_otp(email, otp):
    """Verify if OTP matches the stored one"""
    cache_key = f"email_otp_{email}"
    stored_otp = cache.get(cache_key)
    if stored_otp and stored_otp == otp:
        cache.delete(cache_key)  # Delete OTP after successful verification
        return True
    return False 