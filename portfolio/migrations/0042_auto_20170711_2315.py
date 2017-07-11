# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 23:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0041_auto_20170711_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other', models.CharField(blank=True, max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('collaborators', models.ManyToManyField(to='portfolio.Collaborator')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.Venue')),
            ],
        ),
        migrations.RemoveField(
            model_name='performance',
            name='collaborators',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='venue',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='work',
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='work',
            name='pdf',
            field=models.FileField(blank=True, upload_to='pdfs'),
        ),
        migrations.DeleteModel(
            name='Performance',
        ),
        migrations.AddField(
            model_name='event',
            name='work',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portfolio.Work'),
        ),
    ]
