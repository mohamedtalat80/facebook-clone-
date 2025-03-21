# Generated by Django 4.2.4 on 2023-09-03 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.post')),
                ('user_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('likes_of_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.like')),
                ('post_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.post')),
                ('user_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
