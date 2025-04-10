from rest_framework.permissions import BasePermission

class IsHospitalOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            return request.method in ['GET', 'HEAD', 'OPTIONS']
        return False
