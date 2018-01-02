# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class BlogPosts(models.Model):
    title = models.CharField(max_length=(300),)
    text = models.TextField()
    publish_date = models.DateField()
    #if this is true, then this is the BlogPost that is displayed (no two posts will have the same title)
    to_display = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    """ I am thinking right now that I will have it be a list of posts and I am thinking that she will 
    just select which one she wants to show [granted, she would never show an older post, so maybe I 
    don't even have to save it] """
    
class Links(models.Model):
    title = models.CharField(max_length=(300),)
    link_url = models.URLField()
    description = models.TextField()
    
        