import uuid

from django.db import models

from users.models import User


class Node(models.Model):

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)

    is_active = models.BooleanField(default=False)
    ip = models.URLField(null=True)
    

    def __str__(self):
        return str(self.id)


