from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel

from remote_tutor.tutor.models import Occupation, University, College, School


class Student(SoftDeletableModel, TimeStampedModel):
    user_profile = models.OneToOneField('users.Profile', on_delete=models.SET_NULL, null=True)
    # guardian_phone_number = models.
    guardian_email = models.EmailField(null=True, blank=True)
    #todo:: need to add necessary informations
