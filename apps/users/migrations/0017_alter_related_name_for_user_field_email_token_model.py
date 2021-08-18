# Generated by Django 3.2.6 on 2021-08-11 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0016_alter_related_name_for_user_field_profile_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_email_tokens', to=settings.AUTH_USER_MODEL),
        ),
    ]
