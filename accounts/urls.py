from django.urls import path
from . import views

app_name = 'accounts'  # This is important for namespacing!

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('aadhaar-verification/', views.aadhaar_verification, name='aadhaar_verification'),
    path('logout/', views.logout_view, name='logout'),  # Add this line for logout
]
