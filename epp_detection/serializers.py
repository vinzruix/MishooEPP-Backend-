from typing import Any

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser

from department.serializer import DepartmentSimpleSerializer
from epp_detection.models import EPPNode

class EPPNodeObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        try:
            data = super().validate(attrs)
        except Exception as e:
            raise AuthenticationFailed({"error": "invalid credentials"})

        if not EPPNode.objects.filter(user_node=self.user).exists():
            raise AuthenticationFailed({"error": "invalid credentials"})

        node = EPPNode.objects.get(user_node=self.user)

        if not node.is_active:
            raise AuthenticationFailed({"error": "device not active"})

        return data

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['is_device'] = True
        token['id_node'] = user.username
        token['department'] = DepartmentSimpleSerializer(user.epp_nodes.department).data
        return token


class EPPNodeSerializer(serializers.ModelSerializer):
    department = DepartmentSimpleSerializer()

    class Meta:
        model = EPPNode
        fields = ["id","name","is_active","ip","department"]
