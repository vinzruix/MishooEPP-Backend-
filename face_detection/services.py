import cv2
import face_recognition
import numpy as np

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


def find_worker(encodings):
    for identifier, tensor_faces in User.objects.values_list('id', 'tensor_faces'):
        tensors = np.array(tensor_faces)
        for tensor in tensors:
            result = face_recognition.compare_faces([tensor], encodings[0], tolerance=0.5)

            if result == np.True_:
                return identifier
    return False
