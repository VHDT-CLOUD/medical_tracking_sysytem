from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AadhaarOTP

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        aadhaar_number = data.get("aadhaar_number")

        if len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
            return JsonResponse({"error": "Invalid Aadhaar number"}, status=400)

        otp = AadhaarOTP.generate_otp()
        AadhaarOTP.objects.update_or_create(aadhaar_number=aadhaar_number, defaults={"otp": otp})

        # Simulate OTP sending
        print(f"Mock OTP Sent: {otp}")

        return JsonResponse({"message": "OTP sent successfully"})

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        aadhaar_number = data.get("aadhaar_number")
        otp = data.get("otp")

        otp_record = AadhaarOTP.objects.filter(aadhaar_number=aadhaar_number, otp=otp).first()
        if otp_record:
            otp_record.delete()  # OTP should be one-time use
            return JsonResponse({"message": "OTP verified successfully"})
        return JsonResponse({"error": "Invalid OTP"}, status=400)