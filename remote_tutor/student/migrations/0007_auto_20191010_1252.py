# Generated by Django 2.2.2 on 2019-10-10 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_student_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Profile'),
        ),
    ]
