from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from sympy.codegen.ast import continue_

from users.models import User


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

            try:
                if user.sensor_nodes:
                    node = user.sensor_nodes
            except Exception as e:
                print(e)

            try:
                if user.epp_nodes:
                    node = user.epp_nodes
            except Exception as e:
                print(e)



            if not node.is_active:
                raise PermissionDenied({"error":f"Device not active"})


    return PermissionDynamic