from .models import Message, Notification, MessageHistory
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

@receiver(post_save, sender=Message)
def create_notification(sender, instance, **kwargs):
    Notification.objects.create(User=instance.receiver, message=instance);

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.edited:
        Message.object.update(edited=True)
        MessageHistory.object.update(message=instance)

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # It's a new message, not an edit
        return

    if old_instance.content != instance.content:
        instance.edited = True
        instance.edited_at = timezone.now()

        MessageHistory.objects.create(
            message=instance,
            old_content=old_instance.content,
            edited_at=timezone.now(),
            edited_by=instance.sender,
        )

@receiver(post_delete, sender=User)
def del_user_account(sender, instance, **kwargs):
    # Delete messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications
    Notification.objects.filter(user=instance).delete()

    # Delete message histories
    histories = MessageHistory.objects.filter(
    messages__sender=instance) | MessageHistory.objects.filter(messages__receiver=instance)
    histories.distinct().delete()
