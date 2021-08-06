# Generated by Django 3.2.5 on 2021-08-05 15:08

from django.db import migrations, models

import django_cryptography.fields
import django_otp.util

import apps.users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_challenge_token_returned_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtoken',
            name='challenge_token_generated',
            field=django_cryptography.fields.encrypt(models.CharField(default=django_otp.util.random_hex, max_length=40, validators=[apps.users.utils.token_validator])),
        ),
    ]
