from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel

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

