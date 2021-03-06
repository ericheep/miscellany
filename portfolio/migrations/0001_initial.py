# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-11 01:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('text', models.TextField(blank=True)),
                ('audio', models.FileField(blank=True, upload_to='audio')),
            ],
        ),
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('other', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, null=True)),
                ('abstract', models.TextField(max_length=200)),
                ('text', models.TextField(blank=True)),
                ('created_date', models.DateField()),
                ('featured', models.BooleanField(default=True)),
                ('archive', models.FileField(blank=True, upload_to='archive')),
                ('pdf', models.FileField(blank=True, upload_to='pdfs')),
                ('vimeo', models.URLField(blank=True)),
                ('youtube', models.URLField(blank=True)),
                ('github', models.URLField(blank=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='thumbnails')),
                ('audio', models.ManyToManyField(blank=True, to='portfolio.Audio')),
                ('images', models.ManyToManyField(blank=True, to='portfolio.Image')),
                ('tags', models.ManyToManyField(blank=True, to='portfolio.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.Venue'),
        ),
        migrations.AddField(
            model_name='event',
            name='work',
            field=models.ManyToManyField(blank=True, to='portfolio.Work'),
        ),
    ]
