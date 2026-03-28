from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.

class User(AbstractUser):

    class Meta:
        permissions = [
            ("view_all_user","Can view all the profiles"),
            ("create_user", "Can create new users")
        ]

    tensor_faces = ArrayField(ArrayField(models.FloatField(),size=128), size=50, null=True)
    face = models.ImageField(upload_to='worker_images/', null=True)
    pass