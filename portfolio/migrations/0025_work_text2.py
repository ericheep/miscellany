# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0024_auto_20170612_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='text2',
            field=models.TextField(default='This is some default text'),
            preserve_default=False,
        ),
    ]