from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout  # Import the logout function
import random
import json
from .models import AadhaarOTP
from django.utils.timezone import now
from datetime import timedelta

def index(request):
    return render(request, 'index.html')

def aadhaar_verification(request):
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')
        # Implement your Aadhaar verification logic here
        # For example, check if the Aadhaar number is valid and verified
        # If verified, redirect to the dashboard
        return redirect('accounts:dashboard')
    return render(request, 'aadhaar_verification.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            return redirect('accounts:dashboard')

        return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    
    otp = str(random.randint(100000, 999999))
    request.session['otp'] = otp
    return render(request, 'verify_otp.html')

def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            aadhaar_number = data.get("aadhaar_number")
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"error": "Invalid request data"}, status=400)

        if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
            return JsonResponse({"error": "Invalid Aadhaar number"}, status=400)

        otp = AadhaarOTP.generate_otp()
        AadhaarOTP.objects.update_or_create(
            aadhaar_number=aadhaar_number,
            defaults={"otp": otp, "expires_at": now() + timedelta(minutes=5)}
        )

        print(f"Mock OTP Sent: {otp}")
        return JsonResponse({"message": "OTP sent successfully", "otp": otp})

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')
        request.session['aadhaar_number'] = aadhaar_number
        return redirect('accounts:verify_otp')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)  # Call the imported logout function
    return redirect('accounts:login')  # Redirect to login after logout

def register_view(request):
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')
        
        # Check if the Aadhaar number is valid (e.g., length and digit check)
        if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
            return render(request, 'register.html', {'error': 'Invalid Aadhaar number'})

        # Assuming you have a User model where you want to save the Aadhaar number
        # Save the Aadhaar number to the database
        # Example: User.objects.create(aadhaar_number=aadhaar_number, ...other_fields)

        # Redirect directly to the dashboard after successful registration
        return redirect('accounts:dashboard')
    
    return render(request, 'register.html')
