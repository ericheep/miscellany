# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 09:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0018_auto_20170611_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='discipline',
        ),
        migrations.RemoveField(
            model_name='work',
            name='tags',
        ),
    ]
