# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import MonthlyPosts, Links

admin.site.register(MonthlyPosts)
admin.site.register(Links)
