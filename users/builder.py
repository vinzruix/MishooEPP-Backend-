from abc import ABC, abstractmethod

from MishooEPP_Backend.core.instances import face_recognition
from users.models import User


class UserBuilder(ABC):

    @abstractmethod
    def set_username(self,**kwargs):
        pass

    @abstractmethod
    def set_password(self,**kwargs):
        pass

class WorkerUserBuilder(UserBuilder):

    def __init__(self):
        self._user = User()

    def set_username(self,**kwargs):
        self._user.username = kwargs.get("username")

    def set_password(self,**kwargs):
        self._user.set_password(kwargs.get('password'))

    def set_email(self,**kwargs):
        self._user.email = kwargs.get('email')

    def set_face_encodings(self,**kwargs):
        self._user.tensor_faces = face_recognition.get_encodings_by_video(kwargs.get('video'))

    def set_profile_image(self,**kwargs):
        self._user.face = face_recognition.get_user_image_by_video(kwargs.get('video'))

    def set_department(self,**kwargs):
        self._user.department = kwargs.get('department')

    def build(self):

        self._user.save()
        self._user.groups.add(self._user.department.group)
        return self._user




class Director:
    def __init__(self, builder):
        self._builder = builder

    def createUserWorker(self,**kwargs):
        pass





