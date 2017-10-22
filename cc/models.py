# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class BlogPosts(models.Model):
    title = models.CharField(max_length=(300),)
    text = models.TextField()
    publish_date = models.DateField()
    
class Links(models.Model):
    title = models.CharField(max_length=(300),)
    link_url = models.URLField()
    description = models.TextField()
    
        