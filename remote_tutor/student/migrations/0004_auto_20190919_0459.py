# Generated by Django 2.2.2 on 2019-09-19 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20190909_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='verified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_verifier', to=settings.AUTH_USER_MODEL),
        ),
    ]
