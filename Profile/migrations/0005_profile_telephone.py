# Generated by Django 5.1.2 on 2024-11-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_remove_profile_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='telephone',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]