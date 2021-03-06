# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class MonthlyPosts(models.Model):
    title = models.CharField(max_length=(300),)
    text = models.TextField()
    publish_date = models.DateField(null=True)
    #if this is true, then this is the BlogPost that is displayed (no two posts should have the same title)
    to_display = models.BooleanField(default=False)
    
    def set_post_to_display(self):
        displayedPosts = MonthlyPosts.objects.filter(to_display=True)
        if len(displayedPosts) == 0:
            self.to_display = True
        else:
            for post in displayedPosts:
                post.to_display = False
                post.save()
            self.to_display = True
            
    def __str__(self):
        string = "{0}: {1} || {2}...".format(self.to_display, self.title, self.text[:15])
        return string
    
class Links(models.Model):
    title = models.CharField(max_length=(300),)
    url = models.URLField(unique=False) # this is the source of some confusion
    description = models.TextField()
    
    def __str__(self):
        return "{} : {}".format(self.title, self.url)
    