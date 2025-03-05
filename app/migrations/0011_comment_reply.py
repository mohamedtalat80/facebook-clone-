# Generated by Django 4.2.4 on 2023-09-16 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_comment_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app.comment'),
        ),
    ]
