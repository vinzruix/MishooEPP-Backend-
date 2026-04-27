from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from epp_detection.models import EPPNode


# Create your models here.

class Incidence(models.Model):

    def arrival_image_path(self, filename):
        now = self.datetime
        return f"incidences/{self.node.id}/{now:%Y}/{now.year}{now.month}{now.microsecond}{filename}"

    datetime = models.DateTimeField(default=timezone.now())
    missing_epp = ArrayField(models.CharField(max_length=20), size=10)
    node = models.ForeignKey(EPPNode, related_name="incidences", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=arrival_image_path , null=True)
