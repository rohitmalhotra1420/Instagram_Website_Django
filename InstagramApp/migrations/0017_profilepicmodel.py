# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-28 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InstagramApp', '0016_auto_20170916_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePicModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='user_images')),
                ('image_url', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstagramApp.UserModel')),
            ],
        ),
    ]
