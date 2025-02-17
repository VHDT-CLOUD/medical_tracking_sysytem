from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
    return JsonResponse({"message": "Welcome to the accounts app!"})

def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            aadhaar = data.get("aadhaar")
            password = data.get("password")

            user = authenticate(request, username=aadhaar, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse({"error": "Invalid Aadhaar or password"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def user_register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            aadhaar = data.get("aadhaar")
            password = data.get("password")
            # Implement your registration logic here

            return JsonResponse({"message": "Registration successful"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def dashboard(request):
    # Implement your dashboard logic here
    return JsonResponse({"message": "Welcome to your dashboard!"})

@csrf_exempt
def request_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            aadhaar = data.get("aadhaar")
            # Implement OTP request logic here
            return JsonResponse({"message": "OTP sent successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            otp = data.get("otp")
            # Implement OTP verification logic here
            return JsonResponse({"message": "OTP verified successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
