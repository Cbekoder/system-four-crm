from rest_framework.permissions import BasePermission


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


class IsLogisticAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (
                request.user.role == "admin" and
                request.user.is_active and
                request.user.section == "logistic"
        )


class IsGardenAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (
                request.user.role == "admin" and
                request.user.is_active and
                request.user.section == "garden"
        )


class IsFactoryAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (
                request.user.role == "admin" and
                request.user.is_active and
                request.user.section == "factory"
        )


class IsFridgeAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (
                request.user.role == "admin" and
                request.user.is_active and
                request.user.section == "fridge"
        )
