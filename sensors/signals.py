from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import receiver

from sensors.models import SensorNode
from sensors.services import get_sensor_node


@receiver(post_delete,sender=SensorNode)
def delete_sensor_node(sender,instance,**kwargs):
    if instance.user_node:
        instance.user_node.delete()

@receiver(pre_save, sender=SensorNode)
def sensor_node_handle_is_activated_change(sender,instance,**kwargs):
    try:
        old_node = get_sensor_node(instance.id)
    except ValueError as e:
        return None

    if old_node.is_active != instance.is_active:

        if instance.is_active:
            print("Aca yo hago que se active")

        if not instance.is_active:
            print("Yo lo apago xdxdd")

    return None
