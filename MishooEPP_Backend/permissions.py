from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


def permission_required(perm):
    class PermissionDynamic(BasePermission):
        def has_permission(self, request, view):
            if not request.user.has_perm(perm):
                raise PermissionDenied({"error":f"permission {perm} not found"})
            return True

    return PermissionDynamic