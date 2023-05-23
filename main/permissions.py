from rest_framework import permissions


class IsAdminDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "DELETE" and bool(request.user and request.user.is_staff):
            return True
