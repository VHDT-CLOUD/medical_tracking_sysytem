from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import CustomUser, AadhaarOTP, Patient, Doctor, Hospital, MedicalRecord, MedicalDocument
import re
import logging
import json
import traceback
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
import random
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.cache import cache

# Set up logging
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

def index(request):
    return render(request, 'index.html')

def login_view(request):
    """ View for patient login using Aadhaar number and OTP/password """
    if request.method == "POST":
        aadhaar_number = request.POST.get("aadhaar_number", "").strip()
        password = request.POST.get("password", "").strip()
        otp = request.POST.get("otp", "").strip()
        user_type = request.POST.get("user_type", "patient").strip()
        logger.info(f"Patient login attempt - Aadhaar: {aadhaar_number}, OTP provided: {'Yes' if otp else 'No'}")

        # Validate Aadhaar number format
        if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
            logger.warning(f"Invalid Aadhaar number format: {aadhaar_number}")
            return render(request, "login.html", {"error": "Invalid Aadhaar number format. Must be 12 digits."})

        # Check if user exists and is a patient
        try:
            user = CustomUser.objects.get(aadhaar_number=aadhaar_number)
            if not user.is_patient:
                logger.warning(f"User {aadhaar_number} is not a patient")
                return render(request, "login.html", {"error": "This account is not registered as a patient."})
        except CustomUser.DoesNotExist:
            logger.warning(f"No user found with Aadhaar: {aadhaar_number}")
            return render(request, "login.html", {"error": "No user found with this Aadhaar number."})

        # Handle password and OTP-based login
        if password and otp:
            user = authenticate(username=aadhaar_number, password=password)
            if user:
                otp_entry = AadhaarOTP.objects.filter(aadhaar_number=aadhaar_number, otp=otp).first()
                if otp_entry and not otp_entry.is_expired():
                    login(request, user)
                    request.session["user_id"] = user.id
                    request.session["user_type"] = "patient"
                    otp_entry.delete()
                    logger.info(f"Patient {user.username} logged in successfully with password and OTP.")
                    return redirect('/accounts/dashboard/')
                else:
                    logger.warning(f"Invalid or expired OTP for Aadhaar: {aadhaar_number}")
                    return render(request, "login.html", {"error": "Invalid or expired OTP."})
            else:
                logger.warning(f"Authentication failed for Aadhaar: {aadhaar_number}")
                return render(request, "login.html", {"error": "Invalid Aadhaar number or password."})

        # Handle password-only login
        elif password:
            user = authenticate(username=aadhaar_number, password=password)
            if user:
                login(request, user)
                request.session["user_id"] = user.id
                request.session["user_type"] = "patient"
                logger.info(f"Patient {user.username} logged in successfully with password.")
                return redirect('/accounts/dashboard/')
            else:
                logger.warning(f"Authentication failed for Aadhaar: {aadhaar_number}")
                return render(request, "login.html", {"error": "Invalid Aadhaar number or password."})

        # Handle OTP-only login
        elif otp:
            otp_entry = AadhaarOTP.objects.filter(aadhaar_number=aadhaar_number, otp=otp).first()
            if otp_entry and not otp_entry.is_expired():
                try:
                    user = CustomUser.objects.get(aadhaar_number=aadhaar_number)
                    login(request, user)
                    request.session["user_id"] = user.id
                    request.session["user_type"] = "patient"
                    otp_entry.delete()
                    logger.info(f"Patient {user.username} logged in successfully with OTP only.")
                    return redirect('/accounts/dashboard/')
                except CustomUser.DoesNotExist:
                    logger.warning(f"Valid OTP but no user found for Aadhaar: {aadhaar_number}")
                    return render(request, "login.html", {"error": "No user found with this Aadhaar number."})
            else:
                logger.warning(f"Invalid or expired OTP for Aadhaar: {aadhaar_number}")
                return render(request, "login.html", {"error": "Invalid or expired OTP."})

        # If neither password nor OTP is provided
        else:
            logger.warning(f"Login attempt with no credentials for Aadhaar: {aadhaar_number}")
            return render(request, "login.html", {"error": "Please provide either password or OTP."})

    return render(request, "login.html")

@csrf_protect
def hospital_login_view(request):
    """ View for hospital login using hospital ID, registration number, and password """
    try:
        # Get all hospitals for the dropdown
        hospitals = Hospital.objects.filter(is_active=True)
        
        if request.method == "POST":
            hospital_id = request.POST.get("hospital_id", "").strip()
            registration_number = request.POST.get("registration_number", "").strip()
            password = request.POST.get("password", "").strip()
            logger.info(f"Hospital login attempt - Hospital ID: {hospital_id}, Registration: {registration_number}")

            if not hospital_id or not registration_number or not password:
                logger.warning("Missing required fields for hospital login")
                return render(request, "hospital-login.html", {
                    "error": "All fields are required.",
                    "hospitals": hospitals
                })

            try:
                # Find the hospital by ID
                hospital = Hospital.objects.get(id=hospital_id)
                # Verify registration number
                if hospital.registration_number != registration_number:
                    logger.warning(f"Invalid registration number for hospital {hospital_id}")
                    return render(request, "hospital-login.html", {
                        "error": "Invalid registration number for this hospital.",
                        "hospitals": hospitals
                    })
                
                # Get the user associated with this hospital
                user = hospital.get_user()
                if not user:
                    # Try to find a user with this registration number
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user = User.objects.filter(
                        is_hospital=True, 
                        registration_number=registration_number
                    ).first()
                    
                    if not user:
                        logger.warning(f"No user account found for hospital {hospital_id}")
                        return render(request, "hospital-login.html", {
                            "error": "Hospital user account not found. Please contact administrator.",
                            "hospitals": hospitals
                        })
                    
                    # Update the user's hospital field
                    try:
                        user.hospital = hospital
                        user.save()
                        logger.info(f"Updated hospital relationship for user {user.username}")
                    except Exception as e:
                        logger.error(f"Failed to update hospital relationship: {str(e)}")

                # Authenticate user
                user = authenticate(username=user.username, password=password)
                if user is None:
                    logger.warning(f"Invalid password for hospital user {user.username}")
                    return render(request, "hospital-login.html", {
                        "error": "Invalid password.",
                        "hospitals": hospitals
                    })

                # Login the user
                login(request, user)
                request.session["hospital_id"] = hospital.id
                request.session["hospital_name"] = hospital.name
                request.session["user_type"] = "hospital"
                
                logger.info(f"Login successful for hospital {hospital.name}")
                return redirect('accounts:hospital_dashboard')

            except Hospital.DoesNotExist:
                logger.warning(f"Hospital not found with ID: {hospital_id}")
                return render(request, "hospital-login.html", {
                    "error": "Hospital not found.",
                    "hospitals": hospitals
                })
            except Exception as e:
                logger.error(f"Error during hospital login: {str(e)}")
                return render(request, "hospital-login.html", {
                    "error": "An error occurred during login. Please try again.",
                    "hospitals": hospitals
                })

        return render(request, "hospital-login.html", {"hospitals": hospitals})

    except Exception as e:
        logger.error(f"Error in hospital_login_view: {str(e)}")
        return render(request, "hospital-login.html", {
            "error": "An unexpected error occurred. Please try again.",
            "hospitals": []
        })

@login_required(login_url='/login/')
def dashboard(request):
    """ Dashboard view for patients """
    user = request.user
    logger.info(f"Patient Dashboard - User logged in: aadhaar={user.aadhaar_number}, name={user.username}")

    # Check if user is a patient
    if not user.is_patient:
        if user.is_doctor:
            return redirect('/accounts/doctor_dashboard/')
        return render(request, 'login.html', {'error': 'You are not authorized to access the patient dashboard.'})

    if request.method == 'POST':
        try:
            # Extract form data
            hospital_id = request.POST.get('hospital')
            diagnosis = request.POST.get('diagnosis')
            prescription = request.POST.get('prescription')
            record_date = request.POST.get('record_date')
            notes = request.POST.get('notes')
            document = request.FILES.get('document')

            # Validate required fields
            if not hospital_id or not diagnosis or not record_date:
                return render(request, 'dashboard.html', {'error': 'All required fields must be filled.'})

            # Ensure patient exists
            patient = Patient.objects.get(aadhaar_number=user.aadhaar_number)

            # Create a new MedicalRecord instance
            medical_record = MedicalRecord(
                patient=patient,
                hospital_id=hospital_id,
                diagnosis=diagnosis,
                prescription=prescription,
                record_date=record_date,
                notes=notes
            )
            medical_record.save()

            # Save the uploaded document if provided
            if document:
                MedicalDocument.objects.create(medical_record=medical_record, document=document)

            logger.info("Dashboard - Medical record saved successfully.")
            return redirect('/accounts/dashboard/')  # Redirect to refresh the page
        except Patient.DoesNotExist:
            logger.error("Dashboard - Patient record not found for the user.")
            return render(request, 'dashboard.html', {'error': 'Patient record not found.'})
        except Exception as e:
            logger.error(f"Dashboard - Error saving medical record: {str(e)}")
            return render(request, 'dashboard.html', {'error': 'Failed to save medical record.'})

    # Fetch patient and medical records
    try:
        patient = Patient.objects.get(aadhaar_number=user.aadhaar_number)
        medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-record_date')
    except Patient.DoesNotExist:
        patient = None
        medical_records = []
        logger.info("Dashboard - No patient record found for this user.")

    # Fetch hospitals for the form
    hospitals = Hospital.objects.all()
    context = {
        'user': user,
        'patient': patient,
        'medical_records': medical_records,
        'hospitals': hospitals,
        'personal_info': {
            'name': user.username,
            'date_of_birth': patient.dob if patient else None
        }
    }
    return render(request, 'dashboard.html', context)

def hospital_dashboard(request):
    """ Dashboard view for hospitals """
    try:
        # Check if user is logged in and is a hospital user
        if not request.user.is_authenticated:
            logger.warning("Unauthorized access attempt to hospital dashboard")
            return redirect('/accounts/hospital-login/')
        
        if not request.user.is_hospital:
            logger.warning(f"Non-hospital user {request.user.username} attempted to access hospital dashboard")
            return render(request, 'error.html', {'error': 'You are not authorized to access the hospital dashboard.'})
        
        # Get hospital information from the user's hospital field
        try:
            hospital = request.user.hospital
        except Exception:
            hospital = None
        
        # If hospital is not set in the user model, try to get it from the session
        if not hospital:
            hospital_id = request.session.get('hospital_id')
            if hospital_id:
                try:
                    hospital = Hospital.objects.get(id=hospital_id)
                    # Update the user's hospital field if it's not set
                    try:
                        request.user.hospital = hospital
                        request.user.save()
                        logger.info(f"Updated hospital relationship for user {request.user.username}")
                    except Exception as e:
                        logger.error(f"Failed to update hospital relationship: {str(e)}")
                except Hospital.DoesNotExist:
                    logger.error(f"Hospital record not found for ID {hospital_id}")
                    logout(request)
                    request.session.flush()
                    return render(request, 'hospital-login.html', {
                        'error': 'Hospital record not found. Please contact administrator.',
                        'hospitals': Hospital.objects.filter(is_active=True)
                    })
            else:
                # Try to find a hospital by registration number
                if hasattr(request.user, 'registration_number') and request.user.registration_number:
                    hospital = Hospital.objects.filter(registration_number=request.user.registration_number).first()
                    if hospital:
                        try:
                            request.user.hospital = hospital
                            request.user.save()
                            logger.info(f"Found and linked hospital by registration number for user {request.user.username}")
                        except Exception as e:
                            logger.error(f"Failed to update hospital relationship: {str(e)}")
                    else:
                        logger.error(f"No hospital found with registration number {request.user.registration_number}")
                        return render(request, 'error.html', {'error': 'No hospital associated with your account. Please contact administrator.'})
                else:
                    logger.error(f"No hospital associated with user {request.user.username}")
                    return render(request, 'error.html', {'error': 'No hospital associated with your account. Please contact administrator.'})

        # Get all patients for this hospital
        patients = Patient.objects.filter(hospital=hospital)

        # Get all medical records for this hospital
        medical_records = MedicalRecord.objects.filter(
            patient__hospital=hospital
        ).order_by('-record_date')

        context = {
            'hospital': hospital,
            'patients': patients,
            'medical_records': medical_records
        }
        logger.info(f"Hospital dashboard accessed - Hospital ID: {hospital.id}")
        return render(request, 'hospital_dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in hospital dashboard: {str(e)}")
        return render(request, 'error.html', {'error': "An error occurred while processing your request. Please try again or contact support if the problem persists."})

def logout_view(request):
    user_type = request.session.get('user_type', '')
    logger.info(f"Logout - User type: {user_type}")
    logout(request)
    request.session.flush()  # Ensure session is cleared
    logger.info("User logged out successfully.")
    # Redirect based on user type
    if user_type == 'hospital':
        return redirect('/accounts/hospital-login/')
    else:
        return redirect('/accounts/login/')

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        try:
            # Check if the request is JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                aadhaar_number = data.get('aadhaar_number', '').strip()
                username = data.get('username', '').strip()
                email = data.get('email', '').strip()
                phone = data.get('phone', '').strip()
                password = data.get('password', '').strip()
                otp = data.get('otp', '').strip()
                date_of_birth = data.get('date_of_birth', '').strip()
            else:
                # Handle form data
                aadhaar_number = request.POST.get('aadhaar_number', '').strip()
                username = request.POST.get('username', '').strip()
                email = request.POST.get('email', '').strip()
                phone = request.POST.get('phone', '').strip()
                password = request.POST.get('password', '').strip()
                otp = request.POST.get('otp', '').strip()
                date_of_birth = request.POST.get('date_of_birth', '').strip()

            # Validate required fields
            if not all([aadhaar_number, username, email, phone, password, otp, date_of_birth]):
                return JsonResponse({
                    'success': False, 
                    'error': 'All fields are required.'
                }, status=400)

            # Validate Aadhaar number
            if not re.match(r'^\d{12}$', aadhaar_number):
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid Aadhaar number format. Must be 12 digits.'
                }, status=400)

            # Validate email
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid email address.'
                }, status=400)

            # Validate phone number
            if not re.match(r'^\+?\d{10,15}$', phone):
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid phone number format.'
                }, status=400)

            # Check if user already exists
            if CustomUser.objects.filter(aadhaar_number=aadhaar_number).exists():
                return JsonResponse({
                    'success': False, 
                    'error': 'A user with this Aadhaar number already exists.'
                }, status=400)

            # Validate OTP
            otp_entry = AadhaarOTP.objects.filter(
                aadhaar_number=aadhaar_number, 
                otp=otp
            ).first()
            
            if not otp_entry:
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid OTP. Please request a new OTP.'
                }, status=400)
                
            if otp_entry.is_expired():
                return JsonResponse({
                    'success': False, 
                    'error': 'OTP has expired. Please request a new OTP.'
                }, status=400)

            # Create user
            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    phone=phone,
                    aadhaar_number=aadhaar_number,
                    password=password,
                    is_patient=True
                )

                # Create patient profile
                patient = Patient.objects.create(
                    user=user,
                    aadhaar_number=aadhaar_number,
                    date_of_birth=date_of_birth
                )
                patient.save()

                # Delete OTP entry after successful registration
                otp_entry.delete()

                # Log the user in
                login(request, user)
                request.session["user_id"] = user.id
                request.session["user_type"] = "patient"

                logger.info(f"Registration successful for Aadhaar: {aadhaar_number}")
                return JsonResponse({
                    'success': True, 
                    'message': 'Registration successful! Redirecting to dashboard...',
                    'redirect_url': reverse('accounts:dashboard')
                })

            except Exception as e:
                logger.error(f"Error creating user or patient profile: {str(e)}")
                return JsonResponse({
                    'success': False, 
                    'error': 'Failed to create user account. Please try again.'
                }, status=500)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Error in register_view: {str(e)}")
            return JsonResponse({
                'success': False, 
                'error': 'An error occurred during registration. Please try again.'
            }, status=500)

    return render(request, "register.html")

@csrf_exempt
def aadhaar_verification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aadhaar_number = data.get('aadhaar_number')

            # Validate Aadhaar number format
            if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
                return JsonResponse({'error': 'Invalid Aadhaar number format. Must be 12 digits.'}, status=400)

            # Generate OTP
            otp = random.randint(100000, 999999)
            try:
                # Delete any existing OTP entries for this Aadhaar number
                AadhaarOTP.objects.filter(aadhaar_number=aadhaar_number).delete()

                # Create a new OTP entry
                AadhaarOTP.objects.create(
                    aadhaar_number=aadhaar_number,
                    otp=str(otp),
                    expires_at=now() + timedelta(minutes=5)
                )

                # Log OTP generation
                print(f"\n=== DEBUG: OTP for {aadhaar_number} is {otp} ===\n")
                logger.info(f"OTP {otp} generated for Aadhaar number {aadhaar_number}")

            except Exception as e:
                error_details = traceback.format_exc()
                logger.error(f"Failed to generate OTP for Aadhaar number {aadhaar_number}: {str(e)}\n{error_details}")
                return JsonResponse({'error': 'Failed to generate OTP. Please try again.'}, status=500)

            # Create response with OTP for development
            response = {
                'success': True, 
                'message': 'OTP generated successfully!',
                'debug_otp': str(otp)  # Always include OTP for development
            }
            return JsonResponse(response)
        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"Unexpected error in aadhaar_verification: {str(e)}\n{error_details}")
            return JsonResponse({'error': 'An unexpected error occurred while processing your request.'}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)

            aadhaar_number = data.get('aadhaar_number', '').strip()
            otp = data.get('otp', '').strip()

            # Validate required fields
            if not aadhaar_number or not otp:
                return JsonResponse({'success': False, 'error': 'Aadhaar number and OTP are required'}, status=400)

            # Validate Aadhaar number format
            if not re.match(r'^\d{12}$', aadhaar_number):
                return JsonResponse({'success': False, 'error': 'Invalid Aadhaar number format'}, status=400)

            # Validate OTP format
            if not re.match(r'^\d{6}$', otp):
                return JsonResponse({'success': False, 'error': 'Invalid OTP format'}, status=400)

            # Check rate limiting
            cache_key = f'otp_attempts_{aadhaar_number}'
            attempts = cache.get(cache_key, 0)
            
            if attempts >= 5:
                return JsonResponse({
                    'success': False, 
                    'error': 'Too many attempts. Please try again after 15 minutes.'
                }, status=429)

            # Verify OTP
            otp_entry = AadhaarOTP.objects.filter(aadhaar_number=aadhaar_number, otp=otp).first()
            
            if not otp_entry:
                # Increment failed attempts
                cache.set(cache_key, attempts + 1, 900)  # 15 minutes
                return JsonResponse({'success': False, 'error': 'Invalid OTP'}, status=400)

            if otp_entry.is_expired():
                otp_entry.delete()
                return JsonResponse({'success': False, 'error': 'OTP has expired. Please request a new one.'}, status=400)

            # OTP is valid
            cache.delete(cache_key)  # Clear rate limiting
            otp_entry.delete()  # Remove used OTP
            
            return JsonResponse({
                'success': True,
                'message': 'OTP verified successfully'
            })

        except Exception as e:
            logger.error(f"Error in verify_otp: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred while verifying OTP'
            }, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def reset_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aadhaar_number = data.get('aadhaar_number')
            otp = data.get('otp')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if not aadhaar_number or not otp or not new_password or not confirm_password:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if new_password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)

            otp_entry = AadhaarOTP.objects.filter(aadhaar_number=aadhaar_number, otp=otp).first()
            if not otp_entry or otp_entry.is_expired():
                return JsonResponse({'error': 'Invalid or expired OTP'}, status=400)

            user = get_object_or_404(CustomUser, aadhaar_number=aadhaar_number)
            user.set_password(new_password)
            user.save()
            otp_entry.delete()
            return JsonResponse({'success': True, 'message': 'Password reset successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error in reset_password: {str(e)}")
            return JsonResponse({'error': 'An error occurred'}, status=500)
    else:
        return render(request, 'reset_password.html')

def reset_password_view(request):
    # Placeholder implementation for reset password
    return render(request, 'reset_password.html')

@login_required(login_url='/login/')
@csrf_exempt
def add_medical_record(request):
    if request.method == 'POST':
        try:
            hospital_name = request.POST.get('hospital')
            diagnosis = request.POST.get('diagnosis')
            prescription = request.POST.get('prescription')
            record_date = request.POST.get('record_date')
            notes = request.POST.get('notes')
            document = request.FILES.get('document')

            # Validate required fields
            if not hospital_name or not diagnosis or not record_date:
                return JsonResponse({'success': False, 'error': 'All required fields must be filled.'}, status=400)

            # Create a new MedicalRecord instance
            medical_record = MedicalRecord(
                hospital_name=hospital_name,
                diagnosis=diagnosis,
                prescription=prescription,
                record_date=record_date,
                notes=notes
            )
            medical_record.save()

            # Save the uploaded document if provided
            if document:
                MedicalDocument.objects.create(medical_record=medical_record, document=document)

            logger.info("Medical record added successfully.")
            return JsonResponse({'success': True, 'message': 'Medical record added successfully.'})
        except Exception as e:
            logger.error(f"Error adding medical record: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Failed to add medical record.'}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

def hospital_register_view(request):
    """View for hospital registration"""
    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()
            registration_number = request.POST.get("registration_number", "").strip()
            email = request.POST.get("email", "").strip()
            phone_number = request.POST.get("phone_number", "").strip()
            address = request.POST.get("address", "").strip()
            website = request.POST.get("website", "").strip()
            description = request.POST.get("description", "").strip()
            password = request.POST.get("password", "").strip()
            confirm_password = request.POST.get("confirm_password", "").strip()

            # Validate required fields
            if not all([name, registration_number, email, phone_number, address, password, confirm_password]):
                return render(request, "hospital-register.html", {
                    "error": "All required fields must be filled."
                })

            # Validate password match
            if password != confirm_password:
                return render(request, "hospital-register.html", {
                    "error": "Passwords do not match."
                })

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                return render(request, "hospital-register.html", {
                    "error": "Please enter a valid email address."
                })

            # Check if hospital with same registration number exists
            if Hospital.objects.filter(registration_number=registration_number).exists():
                return render(request, "hospital-register.html", {
                    "error": "A hospital with this registration number already exists."
                })

            # Check if hospital with same email exists
            if Hospital.objects.filter(email=email).exists():
                return render(request, "hospital-register.html", {
                    "error": "A hospital with this email already exists."
                })

            # Create the hospital
            hospital = Hospital.objects.create_hospital(
                name=name,
                email=email,
                address=address,
                registration_number=registration_number,
                phone_number=phone_number,
                website=website if website else None,
                description=description if description else None,
                password=password
            )

            # Log the user in
            user = hospital.get_user()
            if user:
                login(request, user)
                request.session["hospital_id"] = hospital.id
                request.session["hospital_name"] = hospital.name
                request.session["user_type"] = "hospital"
                return redirect('/accounts/hospital-dashboard/')
            else:
                return render(request, "hospital-register.html", {
                    "error": "Hospital created but unable to log in. Please try logging in manually."
                })

        except Exception as e:
            logger.error(f"Error in hospital registration: {str(e)}")
            return render(request, "hospital-register.html", {
                "error": "An error occurred during registration. Please try again."
            })

    return render(request, "hospital-register.html")
