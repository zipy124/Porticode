# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Location, Queue
from django.contrib import admin

admin.site.register(Location)
admin.site.register(Queue)
