from rest_framework.permissions import BasePermission

class IsAdminOrMaintenance(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ["ADMIN", "MAINTENANCE"]
        )

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role in ["ADMIN", "MAINTENANCE"]:
            return True
        return obj.user == request.user