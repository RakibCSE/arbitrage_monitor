# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-10 09:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='ExtendSignup',
        ),
    ]
