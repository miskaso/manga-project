# Generated by Django 5.1.2 on 2024-11-08 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manga', '0005_alter_manga_average_rating_alter_manga_popularity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manga',
            name='chapters',
        ),
        migrations.CreateModel(
            name='ChapterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('data', models.DateTimeField(auto_now=True)),
                ('content', models.FileField(upload_to='files/')),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manga.manga')),
            ],
        ),
    ]