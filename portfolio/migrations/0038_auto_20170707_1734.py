# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 17:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0037_auto_20170707_0453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collaborator',
            old_name='website',
            new_name='url',
        ),
    ]