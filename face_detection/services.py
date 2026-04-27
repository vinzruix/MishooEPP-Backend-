import io
import tempfile
from abc import abstractmethod, ABC
from uniface import EdgeFace, compute_similarity
from uniface.constants import  YOLOv5FaceWeights, EdgeFaceWeights
from uniface.detection import  YOLOv5Face
import cv2
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
from face_detection.exeptions import NumFaceError, NoFacesData, UserNotRegistered
from users.models import User

class FaceLocator(ABC):

    @abstractmethod
    def detect_faces(self, **kwargs):
        pass


class UFFaceLocator(FaceLocator):

    def __init__(self):
        self.detector = YOLOv5Face(
            model_name=YOLOv5FaceWeights.YOLOV5S,
            confidence_threshold=0.6,
            nms_threshold=0.5,
            nms_mode='torchvision',
            providers=None,
        )

    def detect_faces(self, **kwargs):
        locations = self.detector.detect(kwargs.get('image'))

        if len(locations) > 1:
            raise NumFaceError("More than one face in the image")
        if len(locations) < 1:
            raise NumFaceError("No faces detected")

        return locations[0].landmarks




class FaceEncoder(ABC):

    @abstractmethod
    def encode_face(self,**kwargs):
        pass


class UFFaceEncoder(FaceEncoder):

    def __init__(self):
        self._recognizer = EdgeFace(model_name=EdgeFaceWeights.XS_GAMMA_06)

    def encode_face(self, **kwargs):
        return  self._recognizer.get_normalized_embedding(kwargs.get('image'), kwargs.get("locations")).tolist()


class FaceComparer(ABC):

    @abstractmethod
    def compare_faces(self,**kwargs):
        pass



class UFFaceComparer(FaceComparer):

    def __init__(self,tolerance = 0.5):
        self._tolerance = tolerance

    def compare_faces(self,**kwargs):
        result = compute_similarity(kwargs.get("encoding_1"), kwargs.get("encoding_2"), normalized=True)
        if result > 0.5:
            return True
        return False


class VideoProcessor:

    def __init__(self,
                 locator : FaceLocator = None,
                 encoder : FaceEncoder = None
                 ):
        self._locator = locator or UFFaceLocator()
        self._encoder = encoder or UFFaceEncoder()

    def extract_encodings_in_video(self, video):
        cap = cv2.VideoCapture(video)
        encodings = []

        while True:
            ret, frame = cap.read()
            if not ret: break
            try:
                locations = self._locator.detect_faces(image=frame)
            except NumFaceError:
                continue

            if locations.all():
                encodings.append(self._encoder.encode_face(locations=locations, image=frame))

        cap.release()

        return encodings

    def extract_last_video_frame(self, video):
        cap = cv2.VideoCapture(video)
        worker_face = None

        while True:
            ret, frame = cap.read()
            if not ret: break

            worker_face = frame

        cap.release()

        return worker_face


class UserSearcher:

    def __init__(self,
                 comparer : FaceComparer = None,
                 tolerance=0.5
                 ):
        self._comparer = comparer or UFFaceComparer(tolerance)

    def search_user_id(self, user_encoding):

        if not User.objects.exists():
            raise NoFacesData("No workers registered")

        user_encoding = np.array(user_encoding)

        for identifier, db_encodings in User.objects.values_list('id', 'tensor_faces'):

            if not db_encodings:
                continue

            encodings = np.array(db_encodings)


            for encoding in encodings:
                if self._comparer.compare_faces(encoding_1=encoding, encoding_2=user_encoding):
                    return User.objects.get(id=identifier)

        raise UserNotRegistered("User not identified")

    def check_user_registered(self, user_encoding):
        try:
            self.search_user_id(user_encoding)
            return True
        except (UserNotRegistered, NoFacesData):
            return False


class MediaConverter:

    @staticmethod
    def np_to_imageRGB_buffer(np_array, filename):
        image = cv2.cvtColor(np_array, cv2.COLOR_BGR2RGB)
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

    def __init__(self, locator : FaceLocator =None,
                 encoder : FaceEncoder = None,
                 comparer: FaceComparer= None,
                 user_searcher=None,
                 comparer_tolerance=0.5,
                 video_processor=None,
                 media_converter=None,
                 ):

        self._locator = locator or UFFaceLocator()
        self._encoder = encoder or UFFaceEncoder()
        self._comparer = comparer or UFFaceComparer(tolerance=comparer_tolerance)
        self._video_processor = video_processor or VideoProcessor(self._locator, self._encoder)
        self._user_searcher = user_searcher or UserSearcher(self._comparer, comparer_tolerance)
        self._media_converter = media_converter or MediaConverter()

    def get_encodings_by_video(self, video) -> list[float]:
        file = self._handle_video(video)
        return self._video_processor.extract_encodings_in_video(file)

    def get_user_id_by_image(self, image) -> tuple[User, ContentFile]:
        image_np = self._handle_image(image)
        locations = self._locator.detect_faces(image=image_np)
        encoding = self._encoder.encode_face(locations=locations, image=image_np)
        user = self._user_searcher.search_user_id(encoding)
        image_cf = self._media_converter.np_to_imageRGB_buffer(image_np, user.username)

        return user, image_cf

    def get_user_id_by_np_array(self, np_array) -> User:
        return self._user_searcher.search_user_id(np_array)

    def is_user_registered(self, np_array) -> bool:
        return self._user_searcher.check_user_registered(np_array)

    def get_user_image_by_video(self, video, image_name):
        file = self._handle_video(video)
        np_image = self._video_processor.extract_last_video_frame(file)
        return self._media_converter.np_to_imageRGB_buffer(np_image, image_name)

    def _handle_image(self, image):

        if isinstance(image, bytes):
            return self._media_converter.binary_to_np(image)

        if isinstance(image, np.ndarray):
            return image

        if isinstance(image, ContentFile):
            return self._media_converter.binary_to_np(image.read())

        return image

    def _handle_video(self, video):

        if isinstance(video, str):
            return video

        return self._media_converter.video_data_to_video_chunks(video)
