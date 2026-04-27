from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pathlib import Path
from users.models import User


@receiver(post_delete, sender=User)
def handle_user_delete(sender,instance,**kwargs):

    try:
        if instance.face.path:
            Path(instance.face.path).unlink(missing_ok=True)
    except ValueError :
        pass


