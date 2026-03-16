import tempfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer
from users.services import create_user


class UserListCreateAPIView(APIView):

    def post(self, request):
        video = request.FILES['video']
        user = {
            "name": request.data['name'],
            "last_name": request.data['last_name'],
            "email": request.data['email'],
            "username": request.data['username'],
            "password": request.data['password']
        }

        temp_file = tempfile.NamedTemporaryFile(delete=False)

        for chunk in video.chunks():
            temp_file.write(chunk)

        temp_file.close()

        new_user = create_user(user, temp_file.name)

        return Response({"user": new_user.username})

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
            return Response({"error":"DoesNotExist"})





