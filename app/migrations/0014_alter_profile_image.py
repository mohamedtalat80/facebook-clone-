# Generated by Django 4.2.4 on 2023-09-17 22:09

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(height_field='35', upload_to=app.models.profile_image_upload_path, width_field='35'),
        ),
    ]
