# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 23:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0028_images_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Images',
            new_name='Image',
        ),
    ]
