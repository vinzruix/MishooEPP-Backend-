import io
import tempfile
from abc import abstractmethod, ABC

import cv2
import face_recognition
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
from face_recognition import face_locations
from sympy.categories.baseclasses import Class
from torchvision.tv_tensors import Video

from face_detection.exeptions import NumFaceError, NoFacesData, UserNotRegistered
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


### face_recognition facade design pattern try

class FaceLocator:

    def __init__(self, model="hog"):
        self._model = model

    def detect_faces(self,image):
        locations = face_recognition.face_locations(image,model=self._model)

        if len(locations) > 1:
            raise NumFaceError("More than one face detected")

        if len(locations) < 1:
            raise NumFaceError("No faces detected")

        return locations

class FaceEncoder:

    def __init__(self,model="large"):
        self._model = model

    def encode_face(self,locations,image):
        encoding = face_recognition.face_encodings(image,locations, model=self._model)[0].tolist()
        return encoding

class FaceComparer:

    def __init__(self,tolerance=0.5):
        self._tolerance = tolerance

    def compare_faces(self,encoding_1,encoding_2):
        comparison_result = face_recognition.compare_faces([encoding_1], np.array(encoding_2), tolerance=self._tolerance)
        return comparison_result[0]


class VideoProcessor:

    def __init__(self, locator = None, encoder = None):
        self._locator = locator or FaceLocator()
        self._encoder = encoder or FaceEncoder()

    def extract_encodings_in_video(self,video):
        cap = cv2.VideoCapture(video)
        encodings = []

        while True:
            ret, frame = cap.read()
            if not ret: break
            try:
                locations = self._locator.detect_faces(frame)
            except ValueError:
                continue

            if locations:
                encodings.append(self._encoder.encode_face(locations,frame))

        cap.release()

        return encodings

    def extract_last_video_frame(self,video):
        cap = cv2.VideoCapture(video)
        worker_face = None

        while True:
            ret, frame = cap.read()
            if not ret: break

            worker_face = frame

        cap.release()

        return worker_face


class UserSearcher:

    def __init__(self, comparer=None, tolerance=0.5):
        self._comparer = comparer or FaceComparer(tolerance)

    def search_user_id(self, user_encoding):

        if not User.objects.exists():
            raise NoFacesData("No workers registered")

        for identifier, db_encodings in User.objects.values_list('id', 'tensor_faces'):

            if not db_encodings:
                continue

            encodings = np.array(db_encodings)

            for encoding in encodings:
                result = self._comparer.compare_faces(encoding, np.array(user_encoding))

                if result == np.True_:
                    return User.objects.get(id=identifier)

        raise UserNotRegistered("User not identified")



class MediaConverter:

    @staticmethod
    def np_to_imageRGB_buffer(np_array,filename):
        image = cv2.cvtColor(np_array,cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        return ContentFile(buffer.read(), name=f"{filename}.jpg")

    @staticmethod
    def video_data_to_video_chunks(video):
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        for chunk in video.chunks():
            temp_file.write(chunk)

        temp_file.close()

        return temp_file.name

    @staticmethod
    def binary_to_np(binary):
        return cv2.imdecode(np.frombuffer(binary, np.uint8), cv2.IMREAD_COLOR)


class FaceRecognitionFacade:

    def __init__(self,locator=None,
                 encoder=None,
                 comparer=None,
                 user_searcher=None,
                 comparer_tolerance=0.5,
                 video_processor=None,
                 media_converter = None,
                 locator_model="hog",
                 encoder_model="large"):

        self._locator = locator or FaceLocator(locator_model)
        self._encoder = encoder or FaceEncoder(encoder_model)
        self._comparer = comparer or FaceComparer(tolerance=comparer_tolerance)
        self._video_processor = video_processor or VideoProcessor(self._locator,self._encoder)
        self._user_searcher = user_searcher or UserSearcher(self._comparer,comparer_tolerance)
        self._media_converter = media_converter or MediaConverter()

    def get_encodings_by_video(self,video) -> list[float]:
        file = self._handle_video(video)
        return self._video_processor.extract_encodings_in_video(file)

    def get_user_id_by_image(self,image) -> tuple[User,ContentFile]:
        image_np = self._handle_image(image)
        locations = self._locator.detect_faces(image_np)
        encoding = self._encoder.encode_face(locations,image_np)
        user = self._user_searcher.search_user_id(encoding)
        image_cf = self._media_converter.np_to_imageRGB_buffer(image_np,user.username)

        return user, image_cf

    def get_user_image_by_video(self,video,image_name):
        file = self._handle_video(video)
        np_image = self._video_processor.extract_last_video_frame(file)
        return self._media_converter.np_to_imageRGB_buffer(np_image,image_name)

    def _handle_image(self,image):

        if isinstance(image, bytes):
            return self._media_converter.binary_to_np(image)

        if isinstance(image, np.ndarray):
            return image

        if isinstance(image, ContentFile):
            return self._media_converter.binary_to_np(image.read())


        return image


    def _handle_video(self,video):

        if isinstance(video,str):
            return video

        return self._media_converter.video_data_to_video_chunks(video)













