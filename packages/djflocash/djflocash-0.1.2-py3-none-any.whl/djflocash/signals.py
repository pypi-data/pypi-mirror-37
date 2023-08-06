from django.db.models import signals
from django.dispatch import receiver

from . import models


@receiver(signals.pre_save, sender=models.Notification)
def link_payment(sender, **kwargs):
    """try to link notification to payment
    """
    obj = kwargs['instance']
    if obj.payment is None:
        obj.payment = obj.find_payment()
