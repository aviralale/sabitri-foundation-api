from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects,
    but allow anyone to view them.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff


class IsOwnerOrAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request for admin users
        if request.user and request.user.is_staff:
            return True

        # Check if the object has an owner field and if it matches the request user
        if hasattr(obj, "owner"):
            return obj.owner == request.user

        # Default to False
        return False
