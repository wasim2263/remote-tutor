from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel

from remote_tutor.tutor.models import Department, Occupation, University, College, School

GENDER_CHOICES = (
    ('male', _('male')),
    ('female', _('female')),
    ('undefined', _('undefined')),
)


class User(AbstractUser, TimeStampedModel, SoftDeletableModel):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    full_name = CharField(_("Full Name of User"), blank=True, null=True, max_length=555)
    phone_no = CharField(max_length=20, blank=True, null=True)
    gender = CharField(max_length=10, choices=GENDER_CHOICES,
                       default='undefined')

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})


class Profile(TimeStampedModel, SoftDeletableModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date_of_birth = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    current_occupation = models.ForeignKey(Occupation, on_delete=models.PROTECT, null=True)
    current_institute = models.CharField(max_length=255, null=True, blank=True,
                                         help_text="current job or service institute.")
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.PROTECT, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT, null=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name='verified_by')
