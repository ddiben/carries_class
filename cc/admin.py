# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import BlogPosts, Links

admin.site.register(BlogPosts)
admin.site.register(Links)
