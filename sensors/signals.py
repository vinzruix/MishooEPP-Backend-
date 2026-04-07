from django.db.models.signals import post_delete
from django.dispatch import receiver

from sensors.models import SensorNode


@receiver(post_delete,sender=SensorNode)
def delete_sensor_node(sender,instance,**kwargs):
    if instance.user_node:
        instance.user_node.delete()