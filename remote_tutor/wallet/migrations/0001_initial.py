# Generated by Django 2.2.2 on 2019-08-12 04:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('balance', models.DecimalField(decimal_places=8, default=0, max_digits=21)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=21)),
                ('status', models.ImageField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('accepted', 'accepted')], default='pending', upload_to='')),
                ('invoice_number', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=20, null=True, unique=True)),
                ('accepted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.Wallet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=21)),
                ('status', models.ImageField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('accepted', 'accepted')], default='pending', upload_to='')),
                ('invoice_number', models.CharField(max_length=150)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wallet.Wallet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
