from rest_framework import permissions


class IsAdminDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, PUT or OPTIONS requests.
        if request.method in (*permissions.SAFE_METHODS, "PUT"):
            if request.method == "PUT":
                return bool(request.user and request.user.is_staff)
            return True

        elif request.method == "DELETE" and bool(
            request.user and request.user.is_staff
        ):
            return True
