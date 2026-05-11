import secrets

from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import receiver
from rest_framework.exceptions import NotAcceptable

from sensors.models import SensorNode
from sensors.services import  send_server_credentials
from users.models import User


@receiver(post_delete,sender=SensorNode)
def delete_sensor_node(sender,instance,**kwargs):
    if instance.user_node:
        instance.user_node.delete()


@receiver(post_save, sender=SensorNode)
def sensor_node_handle_is_activated_change(sender, instance, **kwargs):

    if instance.is_active:
        print("Aca yo hago que se active")

    if not instance.is_active:
        print("Yo lo apago xdxdd")



