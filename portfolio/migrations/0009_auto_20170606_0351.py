# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 03:51
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_auto_20170606_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='work',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None),
        ),
    ]
