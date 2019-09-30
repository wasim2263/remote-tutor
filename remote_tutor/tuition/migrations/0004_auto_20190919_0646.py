# Generated by Django 2.2.2 on 2019-09-19 06:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0005_preference_salary'),
        ('tuition', '0003_auto_20190919_0459'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuition',
            name='salary',
            field=models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(500)]),
        ),
        migrations.CreateModel(
            name='RequestTutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('message', models.CharField(blank=True, max_length=1000, null=True)),
                ('tuition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tuition.Tuition')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.Tutor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
