import tempfile
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.exceptions import NotFound, NotAcceptable, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from MishooEPP_Backend.permissions import permission_required
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer
from users.services import create_user



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserListCreateAPIView(APIView):


    def get_permissions(self):
        if self.request.method == "GET":
            return [permission_required("users.view_all")()]

        if self.request.method == "POST":
            return [permission_required("users.create_user")]

        return [IsAuthenticated()]

    def post(self, request):

        try:
            video = request.FILES['video']
        except MultiValueDictKeyError:
            raise NotAcceptable({"error": "Video not found"})

        user = {
            "name": request.data['name'],
            "last_name": request.data['last_name'],
            "email": request.data['email'],
            "username": request.data['username'],
            "password": request.data['password'],
            "password_confirmation": request.data['password_confirmation'],
            "department" : request.data['department']
        }

        for key, value in user.items():
            if not value:
                raise NotAcceptable({"error": f"Parameter missing:{key}"})

        temp_file = tempfile.NamedTemporaryFile(delete=False)

        for chunk in video.chunks():
            temp_file.write(chunk)

        temp_file.close()

        try:
            create_user(user, temp_file.name)
        except ValueError as e:
            raise ValidationError({"error": f"{e}"})
        except PermissionError as e:
            raise NotAcceptable({"error": f"{e}"})

        return Response({"success": "Usuario creado"}, status=HTTP_201_CREATED)

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class UserDetailAPIView(APIView):


    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise NotFound({"error": "User does not exist"})

class AllUsersAPIView(APIView):

    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise NotFound({"error": "User does not exist"})