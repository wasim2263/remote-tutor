# Generated by Django 2.2.2 on 2019-09-19 06:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0004_auto_20190919_0459'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='salary',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(500)]),
        ),
    ]
