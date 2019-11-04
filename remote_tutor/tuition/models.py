from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, SoftDeletableModel

from remote_tutor.student.models import Student
from remote_tutor.tutor.models import Tutor, Subject, TUITION_TYPE

TUITION_STATUS_CHOICES = (
    ("active", _("active")),
    ("inactive", _("inactive")),
    ("finished", _("finished")),
    ("disputed", _("disputed")),
)

TUITION_REQUEST_STATUS_CHOICES = (
    ("pending", _("Pending")),
    ("accepted", _("Accepted")),
    ("rejected", _("Rejected"))
)


class Tuition(SoftDeletableModel, TimeStampedModel):
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=TUITION_STATUS_CHOICES, default="active")
    tuition_type = models.CharField(max_length=20, choices=TUITION_TYPE, default="monthly")
    lectures = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1, help_text="lectures per month")
    subject = models.ManyToManyField(Subject)
    salary = models.IntegerField(null=True, default=0, validators=[MinValueValidator(500)])


class Lecture(SoftDeletableModel, TimeStampedModel):
    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(("started", _("started")),
                                                      ("finished", _("finished")),), default="started")


class RequestTuition(SoftDeletableModel, TimeStampedModel):
    tuition=models.ForeignKey(Tuition, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=TUITION_REQUEST_STATUS_CHOICES, default="pending")
    message = models.CharField(max_length=1000, null=True, blank=True)
