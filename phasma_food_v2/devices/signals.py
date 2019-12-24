from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from .models import PhasmaDevice

User = get_user_model()


@receiver(post_save, sender=PhasmaDevice)
def add_phasma_device_to_user(sender: User, instance: PhasmaDevice, created: bool, *args: tuple, **kwargs: dict) -> None:
    """Attach phasma device to user that used it to do measurement."""
    if created:
        user = User.objects.get(email=instance._user)
        user.phasma_device = instance
        user.save()
