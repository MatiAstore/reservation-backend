from rest_framework.permissions import BasePermission
from .request_user import get_request_user_or_fail

class IsAdminOrMaintenance(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ["ADMIN", "MAINTENANCE"]
        )

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = get_request_user_or_fail(request)

        if user.role in ["ADMIN", "MAINTENANCE"]:
            return True
        return obj.user == user