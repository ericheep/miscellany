# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0031_auto_20170624_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='images',
            field=models.ManyToManyField(blank=True, to='portfolio.Image'),
        ),
        migrations.AlterField(
            model_name='work',
            name='tags',
            field=models.ManyToManyField(blank=True, to='portfolio.Tag'),
        ),
        migrations.AlterField(
            model_name='work',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
