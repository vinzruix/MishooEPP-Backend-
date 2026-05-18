from django.db import models

from MishooEPP_Backend.core.models import Node
from department.models import Department
from users.models import User


# Create your models here.


class EPPNode(Node):
    user_node = models.OneToOneField(User, related_name="epp_nodes", on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, related_name="epp_nodes", on_delete=models.CASCADE)

