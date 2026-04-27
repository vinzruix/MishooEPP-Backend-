from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.exceptions import NotFound, NotAcceptable, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from face_detection.exeptions import UserRegistered
from users.models import User
from MishooEPP_Backend.permissions import permission_required
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer
from users.services import create_user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserListCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required("users.view_all_user")()]

        if self.request.method == "POST":
            return [permission_required("users.create_user")()]

        return [IsAuthenticated()]

    @staticmethod
    def post(request):

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
            raise NotAcceptable({"error": f"value missing {e}"})


        for key, value in user.items():
            if not value:
                raise NotAcceptable({"error": f"Parameter empty:{key}"})

        try:
            with transaction.atomic():

                create_user(user, video)

        except (UserRegistered, ValueError) as e:
            raise ValidationError({"error": f"{e}"})
        except PermissionError as e:
            raise NotAcceptable({"error": f"{e}"})

        return Response({"success": "Usuario creado"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def get( request):
        user = User.objects.filter(is_device=False, is_staff=False)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):

    @staticmethod
    def get( request, pk):
        user = get_object_or_404(User.objects.filter(pk=pk))
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)