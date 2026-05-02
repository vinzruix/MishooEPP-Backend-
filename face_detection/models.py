from django.db import models

from MishooEPP_Backend.core.models import Node
from department.models import Department
from users.models import User


class CameraNode(Node):
    user_node = models.OneToOneField(User, related_name="camera_nodes", on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, related_name="camera_nodes", on_delete=models.CASCADE)

