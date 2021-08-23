# Generated by Django 3.2.6 on 2021-08-23 12:08

import apps.users.utils
from django.db import migrations, models
import django_cryptography.fields
import django_otp.util


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_related_name_for_user_field_email_token_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtoken',
            name='challenge_token',
            field=django_cryptography.fields.encrypt(models.CharField(default=django_otp.util.random_hex, max_length=255, validators=[apps.users.utils.token_validator])),
        ),
    ]
