from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel

TUITION_TYPE = (
    ("monthly", "Monthly"),
    ("class_number", "Class Number"),
    ("instant", "Instant"),
    ("contract", "Contract")
)

CLASS_LEVELS = (
    ("class_1", "Class 1"),
    ("class_2", "Class 2"),
    ("class_3", "Class 3"),
    ("class_4", "Class 4"),
    ("class_5", "Class 5"),
    ("class_6", "Class 6"),
    ("class_7", "Class 7"),
    ("class_8", "Class 8"),
    ("class_9", "Class 9"),
    ("class_10", "Class 10"),
    ("class_11", "Class 11"),
    ("class_12", "Class 12"),
    ("o_level", "O Level"),
    ("a_level", "A Level"),
    ("ba", "BA"),
    ("bsc", "BSc"),
    ("bcom", "BCom"),
    ("masters", "Masters")
)


class Category(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Subject(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Department(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

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
    user = models.OneToOneField('users.User', on_delete=models.SET_NULL, null=True)
    nid = models.IntegerField(unique=True, null=True)


class Preference(SoftDeletableModel, TimeStampedModel):
    tutor = models.OneToOneField(Tutor, on_delete=models.CASCADE)
    tuition_type = models.CharField(max_length=20, choices=TUITION_TYPE, default="monthly")
    class_level = ArrayField(models.CharField(max_length=25, choices=CLASS_LEVELS, default="any"))
    subject = models.ManyToManyField(Subject)
    salary = models.IntegerField(default=0, validators=[MinValueValidator(500)])


