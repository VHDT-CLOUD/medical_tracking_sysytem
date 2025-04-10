from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now
from datetime import timedelta  # Import timedelta
from .models import AadhaarOTP

@csrf_exempt
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

        # Simulate OTP sending
        print(f"Mock OTP Sent: {otp}")

        return JsonResponse({"message": "OTP sent successfully"})

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            aadhaar_number = data.get("aadhaar_number")
            otp = data.get("otp")
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"error": "Invalid request data"}, status=400)

        if not aadhaar_number or not otp:
            return JsonResponse({"error": "Aadhaar number and OTP are required"}, status=400)

        otp_record = AadhaarOTP.objects.filter(aadhaar_number=aadhaar_number, otp=otp).first()
        if otp_record:
            if otp_record.expires_at < now():
                return JsonResponse({"error": "OTP has expired"}, status=400)
            otp_record.delete()  # OTP should be one-time use
            return JsonResponse({"message": "OTP verified successfully"})
        
        return JsonResponse({"error": "Invalid OTP"}, status=400)
z