# Generated by Django 4.2.3 on 2023-11-08 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_remove_work_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='mainImage',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
