from django.db import models

from . import codes


class PaymentManager(models.Manager):

    def pending(self):
        """filter payments that are pending.

        A payment is pending if it has a pending notification without any further response

        :return: queryset with only pending payments
        """
        qs = super().get_queryset()
        qs = qs.filter(notifications__status__in=codes.PENDING_STATUS)
        qs = qs.exclude(notifications__status__in=codes.RESOLVED_STATUS)
        return qs
