from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from epp_detection.models import EPPNode
from epp_detection.services import get_epp_node


@receiver(post_delete,sender=EPPNode)
def delete_sensor_node(sender,instance,**kwargs):
    if instance.user_node:
        instance.user_node.delete()

@receiver(pre_save, sender=EPPNode)
def sensor_node_handle_is_activated_change(sender,instance,**kwargs):
    try:
        old_node = get_epp_node(instance.id)
    except ValueError as e:
        return None

    if old_node.is_active != instance.is_active:

        if instance.is_active:
            print("Aca yo hago que se active")

        if not instance.is_active:
            print("Yo lo apago xdxdd")

    return None
