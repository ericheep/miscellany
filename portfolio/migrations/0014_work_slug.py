# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0013_auto_20170608_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield'),
        ),
    ]
