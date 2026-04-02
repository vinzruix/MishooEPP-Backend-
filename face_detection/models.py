from django.db import models

from MishooEPP_Backend.core.models import Node
from users.models import User


class CameraSensor(Node):
    user_node = models.OneToOneField(User, related_name="camera_nodes", on_delete=models.CASCADE, null=True)
