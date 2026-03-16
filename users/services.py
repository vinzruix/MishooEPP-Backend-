
from face_detection.services import obtain_tensors_by_video, obtain_worker_image_by_video
from users.models import User


def create_user(user, video):
    faces = obtain_tensors_by_video(video)

    worker_image = obtain_worker_image_by_video(video, user['username'])


    new_user = User()

    new_user.first_name = user['name']
    new_user.last_name = user['last_name']
    new_user.email = user['email']
    new_user.username = user['username']
    new_user.set_password(user['password'])
    new_user.tensor_faces = faces
    new_user.face = worker_image


    new_user.save()

    return new_user
