from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views  # Import the views module

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),  # Corrected app reference
    path('', views.index, name='index'),  # Ensure views is imported
    path('dashboard/', views.dashboard, name='dashboard'),  # Add direct access to dashboard
    path('login/', views.login_view, name='login'),  # Add direct access to login
    path('logout/', views.logout_view, name='logout'),  # Add direct access to logout
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if hasattr(settings, 'MEDIA_URL') and hasattr(settings, 'MEDIA_ROOT'):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
