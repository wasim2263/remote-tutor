from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel

from remote_tutor.tutor.models import Occupation, University, College, School


class Student(SoftDeletableModel, TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    current_occupation = models.ForeignKey(Occupation, on_delete=models.PROTECT, null=True)
    current_institute = models.CharField(max_length=255, null=True, blank=True,
                                         help_text="current job or service institute.")
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.PROTECT, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT, null=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name="student_verifier")
