# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 04:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_auto_20170606_0351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='location',
        ),
    ]