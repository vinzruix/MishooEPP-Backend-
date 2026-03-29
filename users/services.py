from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError, NotAcceptable

from department.models import Department
from face_detection.services import obtain_tensors_by_video, obtain_worker_image_by_video, find_worker
from users.models import User


def create_user(user, video):

    if User.objects.filter(email=user['email']).exists():
        raise ValueError("Email already registered")

    if User.objects.filter(username=user['username']).exists():
        raise ValueError("Username registered")

    if not check_passwords(password=user['password'], password_confirmation=user['password_confirmation']):
        raise ValueError("Password does not match")

    if not Group.objects.filter(id=user["department"]).exists():
        raise ValueError("Department does not exist")



    faces = obtain_tensors_by_video(video)

    if not faces:
        raise ValueError("No faces detected")

    if find_worker(faces[0]) != -1:
        raise PermissionError("Human already registered")

    worker_image = obtain_worker_image_by_video(video, user['username'])

    department = Department.objects.get(id=user['department'])
    new_user = User()

    new_user.first_name = user['name']
    new_user.last_name = user['last_name']
    new_user.email = user['email']
    new_user.username = user['username']
    new_user.set_password(user['password'])
    new_user.department = department

    new_user.groups.add(department.group)



    new_user.tensor_faces = faces
    new_user.face = worker_image

    new_user.save()

    return new_user


def check_passwords(password,password_confirmation):
    if password_confirmation == password:
        return True

    return False
