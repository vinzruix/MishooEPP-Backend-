
from django.db import models
from django.utils import timezone

from face_detection.models import CameraNode
from users.models import User




class WorkerArrival(models.Model):

    class Meta:
        permissions = [
            ("view_all_workerarrival", "Can view all the arrivals"),
        ]


    def arrival_image_path(self, filename):
        now = self.arrival_timestamp
        return f"arrival_images/{now:%Y}/{self.worker.username}/{now.year}{now.month}{now.microsecond}{filename}"

    worker = models.ForeignKey(User, related_name='worker_arrivals', on_delete=models.CASCADE)
    arrival_timestamp = models.DateTimeField(default=timezone.now)
    arrival_image = models.ImageField(upload_to=arrival_image_path, null= True)
    node = models.ForeignKey(CameraNode, related_name="arrivals", on_delete=models.CASCADE, null=True)
    user_node = models.ForeignKey(User, related_name="arrivals", on_delete=models.DO_NOTHING, null=True)

