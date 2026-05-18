import socket
import tempfile
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.exceptions import NotFound, NotAcceptable, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from MishooEPP_Backend.exeptions import ParameterEmpty
from MishooEPP_Backend.helpers import RequestValidatorHelper
from face_detection.exeptions import UserRegistered
from users.models import User
from MishooEPP_Backend.permissions import permission_required
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer
from users.services import create_user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class UserViewSet(ViewSet):

    def get_permissions(self):
        if self.action == "list":
            return [permission_required("users.view_all_user")()]

        if self.action == "create":
            return [permission_required("users.create_user")()]

        return [IsAuthenticated()]


    @staticmethod
    def list(request):
        user = User.objects.filter(is_device=False, is_staff=False)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):

        try:
            video = request.FILES['video']
            user = {
                "name": request.data['name'],
                "last_name": request.data['last_name'],
                "email": request.data['email'],
                "username": request.data['username'],
                "password": request.data['password'],
                "password_confirmation": request.data['password_confirmation'],
                "department": request.data['department']
            }

        except MultiValueDictKeyError as e:
            raise NotAcceptable({"error": f"Parametro {e} vacio"})

        try:
            with transaction.atomic():

                RequestValidatorHelper.search_empty_parameters(user)
                create_user(user, video)

        except PermissionError as e:
            raise NotAcceptable({"error": f"{e}"})

        except (UserRegistered, ValueError, ParameterEmpty) as e:
            raise ValidationError({"error": f"{e}"})



        return Response({"success": "Usuario creado"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def retrieve(request, pk):

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound({"error": "El usuario no existe"})

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
