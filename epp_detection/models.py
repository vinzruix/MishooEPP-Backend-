from django.db import models

from MishooEPP_Backend.core.models import Node
from users.models import User


# Create your models here.


class EPPNode(Node):
    user_node = models.OneToOneField(User, related_name="EPP_nodes", on_delete=models.CASCADE, null=True)

