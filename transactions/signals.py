from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Notification

@receiver(post_save, sender=Transaction)
def send_payment_notification(sender, instance, created, **kwargs):
    if created and instance.status == 'completed':
        message = f'You have received a payment of {instance.converted_amount} {instance.converted_currency} from {instance.sender.username}.'
        Notification.objects.create(user=instance.receiver, message=message)