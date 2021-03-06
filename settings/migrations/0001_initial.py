# Generated by Django 2.0.3 on 2018-03-11 02:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='User UUID')),
                ('remaining_accrual_days', models.DecimalField(decimal_places=3, max_digits=5)),
                ('annual_accrual_days', models.DecimalField(decimal_places=3, max_digits=5)),
                ('max_allowable_accrual_days', models.IntegerField()),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Last Updated Date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profiles',
                'verbose_name_plural': 'User Profiles',
            },
        ),
    ]
