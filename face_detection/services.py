import io

import cv2
import face_recognition
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
from face_recognition import face_locations

from users.models import User


def obtain_tensors_by_video(video):
    cap = cv2.VideoCapture(video)
    tensors_faces = []

    while True:
        ret, frame = cap.read()
        if not ret: break

        try:
            locations = search_face_in_image(frame)
        except ValueError:
            continue
        

        
        if locations:
            tensors_faces.append(face_recognition.face_encodings(frame, locations)[0].tolist())

    cap.release()

    return tensors_faces


def obtain_worker_image_by_video(video, username):
    cap = cv2.VideoCapture(video)
    worker_face = None

    while True:
        ret, frame = cap.read()
        if not ret: break

        worker_face = frame

    cap.release()

    image = obtain_image_buffer_from_nparray(worker_face, f"{username}")

    return image


def find_worker(encoding):

    if not User.objects.exists():
        return -1

    for identifier, tensor_faces in User.objects.values_list('id', 'tensor_faces'):

        if not tensor_faces:
            continue


        tensors = np.array(tensor_faces)

        for tensor in tensors:
            result = face_recognition.compare_faces([tensor], np.array(encoding), tolerance=0.5)

            if result == np.True_:
                return User.objects.get(id=identifier)

    return -1


def search_face_in_image(image):
    locations = face_recognition.face_locations(image, model="hog")


    if len(locations) < 1:
        raise ValueError("No face detected")

    if len(locations) > 1:
        raise ValueError("More than one face detected")

    return locations

def obtain_encoding_ready_to_use(frame,locations):
    return face_recognition.face_encodings(frame, locations)[0].tolist()


def obtain_image_buffer_from_nparray(np_image, filename):

    image_rgb = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
    image_rgb = Image.fromarray(image_rgb)

    buffer = io.BytesIO()
    image_rgb.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"{filename}.jpg")