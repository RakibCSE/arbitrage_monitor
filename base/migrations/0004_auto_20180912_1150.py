# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-12 05:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=20),
        ),
    ]
