from django.contrib.auth.models import Group
from django.db import models

# Create your models here.

class Department(models.Model):
    class Meta:
        permissions = [
            ("create_department","Can create departments"),
            ("view_all_department", "Can visualize departments")
        ]


    name = models.TextField(max_length=50, unique=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    epp = models.JSONField(default=dict)
