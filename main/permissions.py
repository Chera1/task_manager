from rest_framework import permissions


class IsAdminDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method in ("DELETE", "PUT") and bool(
            request.user and request.user.is_staff
        ):
            return True
