# Generated by Django 2.2.2 on 2019-09-09 04:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tuition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('finished', 'finished'), ('disputed', 'disputed')], default='active', max_length=20)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutor.Tutor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
