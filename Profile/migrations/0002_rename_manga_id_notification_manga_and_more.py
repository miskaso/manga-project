# Generated by Django 5.1.2 on 2024-11-08 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='manga_id',
            new_name='manga',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='data',
            field=models.DateTimeField(auto_now=True),
        ),
    ]