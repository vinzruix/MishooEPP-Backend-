import io

import cv2
import face_recognition
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile

from users.models import User


def obtain_tensors_by_video(video):
    cap = cv2.VideoCapture(video)
    tensors_faces = []

    while True:
        ret, frame = cap.read()
        if not ret: break
        locations = face_recognition.face_locations(frame, model="hog")
        print(locations)
        tensors_faces.append(face_recognition.face_encodings(frame, locations)[0].tolist())

    cap.release()

    return tensors_faces


def obtain_worker_image_by_video(video, name):
    cap = cv2.VideoCapture(video)
    worker_face = None

    while True:
        ret, frame = cap.read()
        if not ret: break

        worker_face = frame

    cap.release()

    worker_face = cv2.cvtColor(worker_face, cv2.COLOR_BGR2RGB)
    worker_face = Image.fromarray(worker_face)


    buffer = io.BytesIO()
    worker_face.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    worker_image = ContentFile(buffer.read(), name=f"{name}.jpg")

    return worker_image



def find_worker(encoding):
    for identifier, tensor_faces in User.objects.values_list('id', 'tensor_faces'):

        tensors = np.array(tensor_faces)

        for tensor in tensors:
            result = face_recognition.compare_faces([tensor], np.array(encoding), tolerance=0.5)

            if result == np.True_:
                return User.objects.get(id=identifier)

    return False
