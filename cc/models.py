# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class BlogPosts(models.Model):
    title = models.CharField(max_length=(300),)
    text = models.TextField()
    publish_date = models.DateField()
    #if this is true, then this is the BlogPost that is displayed (no two posts should have the same title)
    to_display = models.BooleanField(default=False)
    
    def __str__(self):
        string = "{0} || {1}...".format(self.title, self.text[:10])
        return string

    """ Have one displayed, but a drop-down menu that allows the display of any previous month from the school year """
    
class Links(models.Model):
    title = models.CharField(max_length=(300),)
    link_url = models.URLField()
    description = models.TextField()
    
        