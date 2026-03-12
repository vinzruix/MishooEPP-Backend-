import tempfile

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from face_detection.services import obtain_tensors_by_video
from users.models import User
from users.services import create_user


class UserAPI(APIView):

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

        return Response({"user": new_user.username })

@csrf_exempt
def temperatura(request):
    if request.method == "POST":
        return JsonResponse({"response":f"Temperatura registrada en x valor xd"})
