# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-17 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='song_URI',
            field=models.CharField(default='na', help_text='URI of a track', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='song_URI',
            field=models.CharField(default='na', help_text='URI of a track', max_length=100),
            preserve_default=False,
        ),
    ]
