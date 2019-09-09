from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel


class Category(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Subject(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class University(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    # logo

    def __str__(self):
        return self.name


class College(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    # logo

    def __str__(self):
        return self.name


class School(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    # logo

    def __str__(self):
        return self.name


class Occupation(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Tutor(SoftDeletableModel, TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    subject = models.ManyToManyField(Subject)
    current_occupation = models.ForeignKey(Occupation, on_delete=models.PROTECT, null=True)
    current_institute = models.CharField(max_length=255, null=True, blank=True,
                                         help_text="current job or service institute.")
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.PROTECT, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT, null=True)
    verified = models.BooleanField(default=False)
    # verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
    #                                 related_name='verifier')
