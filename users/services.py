from face_detection.services import obtain_tensors_by_video
from users.models import User


def create_user(user, video):
    faces = obtain_tensors_by_video(video)

    new_user = User()

    new_user.name = user['name']
    new_user.last_name = user['last_name']
    new_user.email = user['email']
    new_user.username = user['username']
    new_user.password = user['password']
    new_user.tensor_faces = faces

    new_user.save()

    return new_user
