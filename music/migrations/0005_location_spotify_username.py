# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-17 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20181117_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='spotify_username',
            field=models.CharField(default='harrygthomas98', help_text='Username for Spotify', max_length=100),
            preserve_default=False,
        ),
    ]
