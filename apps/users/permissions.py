from rest_framework.permissions import BasePermission


class IsCEOOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.role in ['ceo', 'admin', 'doctor',
                                      'registrator'] or request.user.is_superuser) and request.user.is_active == "active"


class IsCEO(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "ceo" and request.user.is_active


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "admin" and request.user.is_active