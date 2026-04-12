from rest_framework import status
from rest_framework.exceptions import NotFound, NotAcceptable
from rest_framework.response import Response
from rest_framework.views import APIView
from MishooEPP_Backend.core.instances import face_recognition
from attendance.services import register_attendance_successfully
from face_detection.exeptions import NumFaceError, UserNotRegistered, NoFacesData


class FaceDetectionCreateAPIView(APIView):

    @staticmethod
    def post(request):

        try:
            worker, image = face_recognition.get_user_id_by_image(request.body)
        except (NumFaceError, NoFacesData)as e:
            raise NotAcceptable({"error":f"{e}"})
        except UserNotRegistered as e:
            raise NotFound({"error":f"{e}"})

        register_attendance_successfully(worker, image)

        return Response({"success": f"user identified as {worker.first_name}"}, status=status.HTTP_201_CREATED)


