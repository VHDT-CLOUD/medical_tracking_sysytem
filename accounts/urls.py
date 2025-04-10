from django.urls import path
from . import views  # Correct import statement
from .views import reset_password_view  # Import the reset_password view

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('hospital-register/', views.hospital_register_view, name='hospital_register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('hospital-dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('aadhaar-verification/', views.aadhaar_verification, name='aadhaar_verification'),
    path('request-otp/', views.aadhaar_verification, name='request_otp'),  # Use the same function for both endpoints
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('hospital-login/', views.hospital_login_view, name='hospital_login'),
    path('login/', views.login_view, name='login'),
    path('reset-password/', reset_password_view, name='reset_password'),  # Add this line
]
