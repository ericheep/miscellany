# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0021_auto_20170611_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
    ]