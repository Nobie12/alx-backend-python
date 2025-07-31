from .models import Message, Notification
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Message)
def create_notification(sender, instance, **kwargs):
    Notification.objects.create(User=instance.receiver, Message=instance);