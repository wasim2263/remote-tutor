from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel, SoftDeletableModel

from remote_tutor.student.models import Student
from remote_tutor.tutor.models import Tutor

TUITION_STATUS_CHOICES = (
    ('active', _('active')),
    ('inactive', _('inactive')),
    ('finished', _('finished')),
    ('disputed', _('disputed')),
)


class Tuition(SoftDeletableModel, TimeStampedModel):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=TUITION_STATUS_CHOICES, default='active')

# class Booking(SoftDeletableModel, TimeStampedModel):
