# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-23 05:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_coindetails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coindetails',
            old_name='percentage_change_1h',
            new_name='percent_change_1h',
        ),
        migrations.RenameField(
            model_name='coindetails',
            old_name='percentage_change_24h',
            new_name='percent_change_24h',
        ),
        migrations.RenameField(
            model_name='coindetails',
            old_name='percentage_change_7d',
            new_name='percent_change_7d',
        ),
    ]
