from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


def permission_required(perm):
    class PermissionDynamic(BasePermission):
        def has_permission(self, request, view):
            if not request.user.has_perm(perm):
                raise PermissionDenied({"error":f"permission {perm} not found"})

            if request.user.is_device:
                self.check_device_active(request.user)

            return True

        def check_device_active(self,user):

            node = None

            if user.sensor_nodes:
                node = user.sensor_nodes
            if user.epp_nodes:
                node = user.epp_nodes

            if not node.is_active:
                raise PermissionDenied({"error":f"Device not active"})


    return PermissionDynamic