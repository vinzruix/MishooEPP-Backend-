from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView

from department.models import Department
from department.serializer import DepartmentSimpleSerializer
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSimpleSerializer()

    class Meta:

        model = User
        fields = ["id","username","first_name","last_name","email","password","face","department"]
        extra_kwargs = { "password" : {"write_only" : True}, "face" : {"read_only":True}}


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['permissions'] = list(user.get_all_permissions())
        token['worker'] = UserSerializer(User.objects.get(id=user.id)).data
        return token