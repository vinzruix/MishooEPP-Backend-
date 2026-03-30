
from django.db import models
from django.utils import timezone

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

