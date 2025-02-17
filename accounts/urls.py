from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/request-otp/", views.request_otp, name="request_otp"),
    path("api/verify-otp/", views.verify_otp, name="verify_otp"),
    path("api/register/", views.user_register, name="register"),  # Note: Register path already exists above, you can remove this one
]