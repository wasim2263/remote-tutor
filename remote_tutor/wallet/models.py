from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import RandomCharField

from model_utils.models import TimeStampedModel, SoftDeletableModel

DEPOSIT_WITHDRAWAL_STATUS_CHOICES = (
    ('pending', _('pending')),
    ('rejected', _('rejected')),
    ('accepted', _('accepted')),
)


class Wallet(TimeStampedModel, SoftDeletableModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    balance = models.DecimalField(decimal_places=8, max_digits=21, default=0)


class Deposit(TimeStampedModel, SoftDeletableModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    amount = models.DecimalField(decimal_places=8, max_digits=21)
    status = models.CharField(max_length=20, choices=DEPOSIT_WITHDRAWAL_STATUS_CHOICES, default='pending')
    invoice_number = RandomCharField(length=20, unique=True, blank=True, null=True)


class Withdrawal(TimeStampedModel, SoftDeletableModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=8, max_digits=21)
    status = models.CharField(max_length=20, choices=DEPOSIT_WITHDRAWAL_STATUS_CHOICES, default='pending')
    invoice_number = RandomCharField(length=20, unique=True, blank=True, null=True)
    accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT)
