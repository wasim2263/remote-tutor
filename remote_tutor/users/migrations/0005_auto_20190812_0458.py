# Generated by Django 2.2.2 on 2019-08-12 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190812_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('undefined', 'undefined')], default='undefined', max_length=10),
        ),
    ]
