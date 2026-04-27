from django.core.exceptions import ValidationError

from MishooEPP_Backend.core.instances import face_recognition
from MishooEPP_Backend.core.validator import ValidatorStrategy
from users.models import User


class UserEmailValidator(ValidatorStrategy):
    def validate(self,**kwargs):
        if User.objects.filter(email=kwargs.get('email')).exists():
            raise ValidationError("email duplicado")

class UserUsernameValidator(ValidatorStrategy):
    def validate(self,**kwargs):
        if User.objects.filter(username=kwargs.get('username')).exists():
            raise ValidationError("Username duplicado")

class UserPasswordValidator(ValidatorStrategy):
    def validate(self,**kwargs):
        if kwargs.get('password') != kwargs.get('password_confirmation'):
            raise ValidationError("Username duplicado")


class UserFaceValidator(ValidatorStrategy):
    def validate(self,**kwargs):
        if face_recognition.is_user_registered(kwargs.get('user_face')):
            raise ValidationError("Rostro ya registrado")

