# Generated by Django 5.1.2 on 2024-11-15 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0003_profile_telephone_profile_verification_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='telephone',
        ),
    ]