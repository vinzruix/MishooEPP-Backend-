import io

import cv2
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
from django.http import UnreadablePostError
from rest_framework import status
from rest_framework.exceptions import NotAcceptable, NotFound, Throttled, UnsupportedMediaType
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.services import register_attendance_successfully
from face_detection.services import find_worker, search_face_in_image, obtain_encoding_ready_to_use, \
    obtain_image_buffer_from_nparray


class FaceDetectionCreateAPIView(APIView):


    def post(self,request):

        try:
            frame = cv2.imdecode(np.frombuffer(request.body, np.uint8), cv2.IMREAD_COLOR)
        except UnreadablePostError as e:
            raise UnsupportedMediaType("The media was not found")


        try:
            locations = search_face_in_image(frame)
        except ValueError as e:
            raise NotAcceptable({"error": f"{e}"})


        encodings = obtain_encoding_ready_to_use(frame, locations)

        worker = find_worker(encodings)


        if worker:
            image = obtain_image_buffer_from_nparray(frame,f"{worker.username}")
            register_attendance_successfully(worker, image)

            return Response({"success": f"user identified as {worker.first_name}"}, status=status.HTTP_302_FOUND)

        raise NotFound({"error":f"User not identified"})

