# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 21:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0049_auto_20170713_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='collaborators',
        ),
        migrations.RemoveField(
            model_name='event',
            name='other',
        ),
        migrations.RemoveField(
            model_name='image',
            name='image_type',
        ),
    ]
