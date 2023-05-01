from rest_framework.permissions import BasePermission


class IsManagerUser(BasePermission):
    """
    Allows access only if user is a manager.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            request.user.is_manager
            return request.user

class IsAdminUser(BasePermission):
    """
    Allows access only if user is a manager.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            request.user.is_admin
            return request.user