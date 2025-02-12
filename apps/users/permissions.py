from rest_framework.permissions import BasePermission



class IsCEOOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "ceo" or request.user.is_active

    def has_object_permission(self, request, view, obj):
        if request.user.role == "ceo":
            return True

        app_label = obj._meta.app_label
        print(app_label)
        return request.user.role == "admin" and request.user.section == app_label

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