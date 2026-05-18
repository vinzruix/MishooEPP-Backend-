from django.contrib.auth.models import Group

from MishooEPP_Backend.core.instances import face_recognition
from department.models import Department
from face_detection.exeptions import UserRegistered
from users.factory import WorkerCreator
from users.models import User


def create_user(user, video):

    if User.objects.filter(email=user['email']).exists():
        raise ValueError("Email already registered")

    if User.objects.filter(username=user['username']).exists():
        raise ValueError("Username registered")

    if not check_passwords(password=user['password'], password_confirmation=user['password_confirmation']):
        raise ValueError("Password does not match")



    if not Department.objects.filter(pk=user["department"]).exists():
        raise ValueError("Department does not exist")

    faces = face_recognition.get_encodings_by_video(video)

    if not faces:
        raise ValueError("No faces detected")

    for face in faces:
        if  face_recognition.is_user_registered(face):
            raise UserRegistered("User already registered")

    worker_image = face_recognition.get_user_image_by_video(video, user['username'])


    new_user = WorkerCreator().register(name=user["name"],
                           last_name=user["last_name"],
                           email=user["email"],
                           username=user["username"],
                           password=user["password"],
                           department=Department.objects.get(pk=user["department"]),
                           faces=faces,
                           face=worker_image,
                           )

    return new_user


def check_passwords(password, password_confirmation):
    if password_confirmation == password:
        return True

    return False

